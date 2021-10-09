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

    # get all sections
    top_section = tree.select('section.tabdiv')[0]
    details_section, bottom_section = tree.select('.user_detail')
    left_section, middle_section, right_section = details_section.select('.col-sm-4')

    top_section_values = [dt.text.strip() for dt in top_section.select('dt')]
    left_section_values = [dt.text.strip() for dt in left_section.select('dt')]
    middle_section_values = [dt.text.strip() for dt in middle_section.select('dt')]
    right_section_values = [dt.text.strip() for dt in right_section.select('dt')]
    bottom_section_values = [dd.text for dd in bottom_section.select('dd')]

    gender_age = top_section_values[0].split('|')
    gender, age = value_mappers.get_gender(gender_age[0].strip()), int(gender_age[1])

    profiles_info_head = top_section.select('.profiles_info_head')[0]

    # general info
    profile_data = {
        'url': url,
        'name': profiles_info_head.select('h3')[0].text,
        'description': profiles_info_head.select('p')[0].text,
        'gender': gender,
        'age': age,
        'country': top_section_values[1],
        'city': top_section_values[2],
        'state': top_section_values[3],
        'height': get_height_cm(top_section_values[4]),
        'image_urls': '|'.join([img.attrs['src']
                                for img in top_section.select('div.tooltip-img img')]),
        # left section
        'eye_color': value_mappers.get_eye_color(left_section_values[1]),
        'body_type': value_mappers.get_body_type(left_section_values[2]),
        'hair_color': value_mappers.get_hair_color(left_section_values[3]),
        'ethnicity': value_mappers.get_ethnicity(left_section_values[4]),
        'denomination': value_mappers.get_denomination(left_section_values[5]),
        # middle section
        'looking_for': value_mappers.get_looking_for(middle_section_values[0]),
        'church_name': middle_section_values[1],
        'church_attendance': value_mappers.get_church_attendance(middle_section_values[2]),
        'church_raised_in': middle_section_values[3],
        'drink': value_mappers.get_drink(middle_section_values[4]),
        'smoke': value_mappers.get_smoke(middle_section_values[5]),
        # right section
        'willing_to_relocate': value_mappers.get_willing_to_relocate(right_section_values[0]),
        'marital_status': value_mappers.get_marital_status(right_section_values[1]),
        'have_children': value_mappers.get_user_with_children(right_section_values[2]),
        'want_children': value_mappers.get_user_wants_children(right_section_values[3]),
        'education_level': value_mappers.get_education_level(right_section_values[4]),
        'profession': right_section_values[5],
        # bottom section
        'interests': bottom_section_values[0],
        'about_me': bottom_section_values[1].strip(),
        'first_date': bottom_section_values[2],
        'account_settings_criteria': '|'.join(bottom_section_values[3:]),
    }

    return Profile(**profile_data)


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
