import logging
import time

from bs4 import BeautifulSoup

import requests
from requests_futures.sessions import FuturesSession

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from com.dreamlab.profile_scrape.parser.profile import ProfilePageParser
from model.entity_base import Base

from scrape.cookies import CookieJarBlockPolicy
from common.config import read_config


logging.basicConfig(filename='scrape.log',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger('profile_scrape')


def handle_profile_parse_exc(request, exception):
    msg = 'Error retrieving' + request.url + str(exception)
    logger.error(msg)
    print(msg)


def get_profile_links(result_page_html):

    tree = BeautifulSoup(result_page_html, 'html.parser')
    prof_boxes = tree.select('div.user-grid-list.clearfix.clear_margin article')

    return [art.a['href'] for art in prof_boxes]


def get_countries():
    r = requests.get('https://www.christiandatingforfree.com/basic_search.php?'
                     'u_seeking=Female&age_from=18&age_to=26&u_looking_for_value=0&'
                     'u_country=30&u_state=&u_city=&u_postalcode=&distance=&dest=&'
                     'Submit=Submit')

    tree = BeautifulSoup(r.text, 'html.parser')
    return {opt['value']: opt.text for opt in tree.select('#u_country option')}


def build_url(url, params):

    if not params:
        return url

    url += '?'
    for key, val in params.items():
        if val is not None:
            url += '{}={}&'.format(key, val)

    return url[:len(url)-1]


def start_scraping():

    RESULTS_PER_PAGE = 12

    config = read_config()

    logger.info("Starting SQL engine")

    engine = create_engine(config.db_url, echo=False)
    Base.metadata.create_all(engine)
    DbSession = sessionmaker(bind=engine)
    db_session = DbSession()

    users_per_batch = 12

    session = requests.Session()
    session.cookies.set_policy(CookieJarBlockPolicy())
    session = FuturesSession(session=session, max_workers=users_per_batch + 1)

    url_params = {
        'age_from': 18,
        'age_to': 99,
        'u_seeking': None,
        'u_looking_for_value': 0,
        'u_country': 0
    }

    search_response = session.get(build_url('https://www.christiandatingforfree.com/basic_search.php', url_params))

    url_params['start'] = 0

    total_users_processed = 0

    page_parser = ProfilePageParser()

    while True:

        page_no = url_params['start'] // RESULTS_PER_PAGE + 1
        print('Processing page', page_no)

        links = get_profile_links(search_response.result().text)
        if not links:
            # no links found on the page means we have gone to the end of the results, leave the loop
            break

        futures = [session.get(l) for l in links]

        url_params['start'] += RESULTS_PER_PAGE
        search_response = session.get(build_url('https://www.christiandatingforfree.com/basic_search.php', url_params))

        for f in futures:

            # wait a 100 ms, so the firewall doesn't catch us
            time.sleep(0.1)

            r = f.result()
            try:
                db_session.add(page_parser.parse(r.text))
                total_users_processed += 1
            except Exception as e:
                msg = f'Failed to scrape url {r.url}. Reason: {e}'
                logger.info(msg)
                print(msg)

        db_session.commit()
        print('Users processed till now:', total_users_processed)

    print('Done')
    logging.shutdown()
