import logging
import time

from requests_futures.sessions import FuturesSession
from requests import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.entity_base import Base
from scrape import profile_scrape
from scrape.cookies import CookieJarBlockPolicy


logging.basicConfig(filename='scrape.log',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger('profile_scrape')


def handle_profile_parse_exc(request, exception):
    msg = 'Error retrieving' + request.url + str(exception)
    logger.error(msg)
    print(msg)


RESULTS_PER_PAGE = 12


def build_url(url, params):

    if not params:
        return url

    url += '?'
    for key, val in params.items():
        if val is not None:
            url += '{}={}&'.format(key, val)

    return url[:len(url)-1]


def main():

    logger.info("Starting SQL engine")

    engine = create_engine('mysql+mysqlconnector://moblytics:moblytics@192.168.68.128:3306/moblytics', echo=False)
    Base.metadata.create_all(engine)
    DbSession = sessionmaker(bind=engine)
    db_session = DbSession()

    users_per_batch = 12

    session = Session()
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
    while True:

        page_no = url_params['start'] // RESULTS_PER_PAGE + 1
        print('Processing page', page_no)

        links = profile_scrape.get_profile_links(search_response.result().text)
        if not links:
            # no links found on the page means we have gone to the end of the results, leave the loop
            break

        futures = [session.get(l) for l in links]

        url_params['start'] += RESULTS_PER_PAGE
        search_response = session.get(build_url('https://www.christiandatingforfree.com/basic_search.php', url_params))

        for f in futures:
            try:
                # wait a 100 ms, so the firewall doesn't catch us
                time.sleep(0.1)

                r = f.result()
                db_session.add(profile_scrape.parse_profile_page(r.url, r.text))
                total_users_processed += 1

            except ValueError as e:
                msg = str(e)
                logger.info(msg)
                print(msg)

        db_session.commit()
        print('Users processed till now:', total_users_processed)

    print('Done')
    logging.shutdown()


if __name__ == '__main__':
    main()
