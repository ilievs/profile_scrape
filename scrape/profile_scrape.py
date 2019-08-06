import logging
import time

from bs4 import BeautifulSoup

import requests
from requests_futures.sessions import FuturesSession

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.profile import *
from model.entity_base import Base

import scrape.value_mappers as value_mappers
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


def get_height_cm(feet_inches_str):
    parts = feet_inches_str.split("'")
    if len(parts) < 2:
        return 0

    feet, inches = parts
    return int(int(feet) * 30.48 + int(inches[:-1]) * 2.54)


def parse_profile_page(url, page_html):
    tree = BeautifulSoup(page_html, 'html.parser')
    sections = tree.select('#wrapper div.maincontainer main section.sectionspace')
    if not sections:
        raise ValueError('Account deleted, not activated, or non-existent:', url)

    profile_container = sections[0]
    first_dts = profile_container.select('div.row:nth-of-type(1) dt')
    values = [dt.text.strip() for dt in first_dts]

    second_values = [dt.text
                     for boxes in tree.select('div.whitelinebox.responsive_block')[2:]
                     for dt in boxes.select('dt')]

    additional_texts = [dd.text.strip() for dd in tree.select('.whitelinebox2.responsive_block.clearfix dd')]
    interests = additional_texts[0] if additional_texts[0] != '' else None
    about_me = additional_texts[1] if additional_texts[1] != '' else None
    first_date = additional_texts[2] if additional_texts[2] != '' else None
    account_settings_criteria = additional_texts[3] if additional_texts[3] != '' else None

    profile = Profile(
        url=url,
        gender=value_mappers.get_gender(values[0]),
        country=values[1],
        city=values[2],
        state=values[3],
        height_cm=get_height_cm(values[4]),
        age=int(values[6]),
        eye_color=value_mappers.get_eye_color(values[7]),
        body_type=value_mappers.get_body_type(values[8]),
        hair_color=value_mappers.get_hair_color(values[9]),
        ethnicity=value_mappers.get_ethnicity(values[10]),
        denomination=value_mappers.get_denomination(values[11]),
        photo_urls='|'.join([img['src'] for img in tree.select('div.tooltip-img img')]),
        looking_for=value_mappers.get_looking_for(second_values[0]),
        church_name=second_values[1],
        church_attendance=value_mappers.get_church_attendance(second_values[2]),
        church_raised_in=second_values[3],
        drink=value_mappers.get_drink(second_values[4]),
        smoke=value_mappers.get_smoke(second_values[5]),
        willing_to_relocate=value_mappers.get_willing_to_relocate(second_values[6]),
        marital_status=value_mappers.get_marital_status(second_values[7]),
        have_children=value_mappers.get_user_with_children(second_values[8]),
        want_children=value_mappers.get_user_wants_children(second_values[9]),
        education_level=value_mappers.get_education_level(second_values[10]),
        profession=second_values[11],
        interests=interests,
        about_me=about_me,
        first_date=first_date,
        account_settings_criteria=account_settings_criteria)

    return profile


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
            try:
                # wait a 100 ms, so the firewall doesn't catch us
                time.sleep(0.1)

                r = f.result()
                db_session.add(parse_profile_page(r.url, r.text))
                total_users_processed += 1

            except ValueError as e:
                msg = str(e)
                logger.info(msg)
                print(msg)

        db_session.commit()
        print('Users processed till now:', total_users_processed)

    print('Done')
    logging.shutdown()
