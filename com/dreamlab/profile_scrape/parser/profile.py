from bs4 import BeautifulSoup

import scrape.value_mappers as value_mappers
from com.dreamlab.profile_scrape.parser.page_parser import PageParser
from model.profile import Profile


def get_height_cm(feet_inches_str):
    parts = feet_inches_str.split("'")
    if len(parts) < 2:
        return 0

    feet, inches = parts
    return int(int(feet) * 30.48 + int(inches[:-1]) * 2.54)


class ProfilePageParser(PageParser):

    def parse(self, html):
        tree = BeautifulSoup(html, 'html.parser')

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

        url = tree.select('.profilelist')[0].attrs('href')

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
