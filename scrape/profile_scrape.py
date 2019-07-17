import os

from bs4 import BeautifulSoup
import requests

import model.profile as date_profile


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
        raise ValueError('Account delete, not activated, or non-existent:', url)

    profile_container = sections[0]
    first_dts = profile_container.select('div.row:nth-of-type(1) dt')
    values = [dt.text.strip() for dt in first_dts]

    second_values = [dt.text for boxes in tree.select('div.whitelinebox.responsive_block')[2:] for dt in boxes.select('dt')]

    additional_texts = [dd.text.strip() for dd in tree.select('.whitelinebox2.responsive_block.clearfix dd')]
    interests = additional_texts[0] if additional_texts[0] != '' else None
    about_me = additional_texts[1] if additional_texts[1] != '' else None
    first_date = additional_texts[2] if additional_texts[2] != '' else None
    account_settings_criteria = additional_texts[3] if additional_texts[3] != '' else None

    profile = date_profile.Profile(
        url=url,
        gender=values[0],
        country=values[1],
        city=values[2],
        state=values[3],
        height_cm=get_height_cm(values[4]),
        age=int(values[6]),
        eye_color=values[7],
        body_type=values[8],
        hair_color=values[9],
        ethnicity=values[10],
        denomination=values[11],
        photo_urls='|'.join([img['src'] for img in tree.select('div.tooltip-img img')]),
        looking_for=second_values[0],
        church_name=second_values[1],
        church_attendance=second_values[2],
        church_raised_in=second_values[3],
        drink=second_values[4],
        smoke=second_values[5],
        willing_to_relocate=second_values[6],
        marital_status=second_values[7],
        have_children=second_values[8],
        want_children=second_values[9],
        education_level=second_values[10],
        profession=second_values[11],
        interests=interests,
        about_me=about_me,
        first_date=first_date,
        account_settings_criteria=account_settings_criteria)

    return profile


def download_photos(profile, path):

    if not profile.photo_urls:
        return

    if not os.path.exists(path):
        os.mkdir(path)

    for url in profile.photo_urls.split('|'):
        r = requests.get(url)
        file_path = 'photos/' + url.split('/')[-1]
        if not os.path.isfile(file_path):
            with open(file_path, mode='w+b') as f:
                f.write(r.content)


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
