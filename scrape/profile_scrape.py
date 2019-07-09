import os

from bs4 import BeautifulSoup
import requests

import model.profile as date_profile

search_to_url_param_country_mappings = {
    'Niue': '157',
    'Luxembourg': '124',
    'Ireland': '103',
    'Anguilla': '7',
    'Jordan': '108',
    'United Arab Emirates': '221',
    'Chad': '42',
    'Swaziland': '202',
    'Nauru': '148',
    'Mauritania': '135',
    'Mozambique': '145',
    'Honduras': '95',
    'Austria': '14',
    'Libyan Arab Jamahiriya': '121',
    'Germany': '81',
    'Chile': '43',
    'Italy': '105',
    'Wallis and Futuna Islands': '233',
    'Croatia': '53',
    'Tokelau': '211',
    'Vanuatu': '227',
    'American Samoa': '4',
    'Tunisia': '214',
    'Maldives': '130',
    'Djibouti': '58',
    'Malawi': '128',
    'Madagascar': '127',
    'Brazil': '30',
    'Thailand': '209',
    'Rwanda': '177',
    'Aruba': '12',
    'Greenland': '85',
    'Ecuador': '62',
    'South Africa': '193',
    'Cocos (Keeling) Islands': '46',
    'Turks and Caicos Islands': '217',
    'Brunei Darussalam': '32',
    'Liechtenstein': '122',
    'Australia': '13',
    'St. Pierre and Miquelon': '198',
    'Andorra': '5',
    'Saudi Arabia': '184',
    'Solomon Islands': '191',
    'Belize': '22',
    'Mexico': '138',
    'United States': '1',
    'Norway': '160',
    'Lithuania': '123',
    'Mongolia': '142',
    'Dominica': '59',
    'Syrian Arab Republic': '205',
    'Western Sahara': '234',
    'Iraq': '102',
    'Guam': '88',
    'India': '99',
    'Ghana': '82',
    'Bermuda': '24',
    'Nepal': '149',
    'Virgin Islands (U.S.)': '232',
    'Tonga': '212',
    'Saint Vincent and the Grenadines': '180',
    'Uzbekistan': '226',
    'Bulgaria': '33',
    'Viet Nam': '230',
    'Tanzania, United Republic of': '208',
    'Denmark': '57',
    'Netherlands': '150',
    'Albania': '2',
    'Guinea': '90',
    'Taiwan': '206',
    'Bahamas': '16',
    'Algeria': '3',
    'Malta': '132',
    "Cote D'Ivoire": '52',
    'Indonesia': '100',
    'Malaysia': '129',
    'Congo': '49',
    'Togo': '210',
    'Bangladesh': '18',
    'Netherlands Antilles': '151',
    'Liberia': '120',
    'Bouvet Island': '29',
    'Sudan': '199',
    'Yemen': '235',
    'Northern Mariana Islands': '159',
    'Comoros': '48',
    'Paraguay': '166',
    'Trinidad and Tobago': '213',
    'Suriname': '200',
    'Afghanistan': '223',
    'Gambia': '79',
    'San Marino': '182',
    'Antigua and Barbuda': '9',
    'Mauritius': '136',
    'Greece': '84',
    'Niger': '155',
    'Bolivia': '26',
    'Uruguay': '225',
    'Grenada': '86',
    'Ethiopia': '68',
    'Singapore': '188',
    'Guyana': '92',
    'Portugal': '171',
    'Senegal': '185',
    'Japan': '107',
    'Turkey': '215',
    'Vatican City State (Holy See)': '228',
    'Zaire': '237',
    'Sweden': '203',
    'France': '73',
    'Bhutan': '25',
    'Slovenia': '190',
    'Dominican Republic': '60',
    'Kiribati': '111',
    "Lao People's Democratic Republic": '116',
    'Gabon': '78',
    'Equatorial Guinea': '65',
    'Fiji': '71',
    'Hungary': '97',
    'Lebanon': '118',
    'Belgium': '21',
    'Switzerland': '204',
    'Iceland': '98',
    'Slovakia (Slovak Republic)': '189',
    'Seychelles': '186',
    'South Korea': '113',
    'Czech Republic': '56',
    'Egypt': '63',
    'Georgia': '80',
    'East Timor': '61',
    'Latvia': '117',
    'Armenia': '11',
    'Cook Islands': '50',
    'Lesotho': '119',
    'Reunion': '174',
    'Tuvalu': '218',
    'Qatar': '173',
    'Pitcairn': '169',
    'Martinique': '134',
    'Bahrain': '17',
    'Venezuela': '229',
    'Moldova, Republic of': '140',
    'Argentina': '10',
    'Mayotte': '137',
    'Cape Verde': '39',
    'Central African Republic': '41',
    'Papua New Guinea': '165',
    'Cuba': '54',
    'Jamaica': '106',
    'Sierra Leone': '187',
    'Romania': '175',
    'Spain': '195',
    'Svalbard and Jan Mayen Islands': '201',
    'Gibraltar': '83',
    'Peru': '167',
    'United Kingdom': '222',
    'All Countries': '0',
    'Turkmenistan': '216',
    'Burkina Faso': '34',
    'Finland': '72',
    'Mali': '131',
    'Zambia': '238',
    'Saint Kitts and Nevis': '178',
    'Iran (Islamic Republic of)': '101',
    'Angola': '6',
    'Namibia': '147',
    'Guatemala': '89',
    'Faroe Islands': '70',
    'Russian Federation': '176',
    'Norfolk Island': '158',
    'Kazakhstan': '109',
    'China': '44',
    'British Indian Ocean Territory': '31',
    'Barbados': '19',
    'Morocco': '144',
    'Burundi': '35',
    'Sri Lanka': '196',
    'Benin': '23',
    'South Georgia and the South Sandwich Islands': '194',
    'Haiti': '93',
    'Guinea-bissau': '91',
    'Nicaragua': '154',
    'Ukraine': '220',
    'Monaco': '141',
    'Botswana': '28',
    'Cambodia': '36',
    'Canada': '38',
    'Pakistan': '162',
    'Estonia': '67',
    'Bosnia and Herzegowina': '27',
    'Virgin Islands (British)': '231',
    'Yugoslavia': '236',
    'Puerto Rico': '172',
    'New Zealand': '153',
    'French Guiana': '75',
    'Philippines': '168',
    'Marshall Islands': '133',
    'Colombia': '47',
    'Cyprus': '55',
    'Kuwait': '114',
    'Tajikistan': '207',
    'Kyrgyzstan': '115',
    'Falkland Islands (Malvinas)': '69',
    'Costa Rica': '51',
    'Heard and Mc Donald Islands': '94',
    'Nigeria': '156',
    'France, Metropolitan': '74',
    'Micronesia, Federated States of': '139',
    'Antarctica': '8',
    'Christmas Island': '45',
    'Montserrat': '143',
    'Hong Kong': '96',
    'Somalia': '192',
    'Guadeloupe': '87',
    'New Caledonia': '152',
    'Kenya': '110',
    'Poland': '170',
    'Zimbabwe': '239',
    'Azerbaijan': '15',
    'Belarus': '20',
    'Cayman Islands': '40',
    'Macedonia, The Former Yugoslav Republic of': '126',
    'Oman': '161',
    'Macau': '125',
    'French Polynesia': '76',
    'Panama': '164',
    'French Southern Territories': '77',
    'Palau': '163',
    'Uganda': '219',
    'Israel': '104',
    'Eritrea': '66',
    'Cameroon': '37',
    'El Salvador': '64',
    'Samoa': '181',
    'Myanmar': '146',
    'Saint Lucia': '179',
    'St. Helena': '197',
    'Sao Tome and Principe': '183'
}

url_param_key_mappings = {
    'seeking': 'u_seeking',
    'fromAge': 'age_from',
    'toAge': 'age_to',
    'country': 'u_country',
}

search_to_url_param_seeking_mapping = {
    'male': 'Male',
    'female': 'Female'
}

search_to_url_param_value_mappings = {
    **search_to_url_param_country_mappings,
    **search_to_url_param_seeking_mapping
}


def get_url_params(search_params):
    url_params = {
        url_param_key_mappings[key]:
            search_to_url_param_value_mappings[value] if key in ['seeking'] else value
        for key, value in search_params.items()
    }

    return url_params


def get_height_cm(feet_inches_str):
    parts = feet_inches_str.split("'")
    if len(parts) < 2:
        return 0

    feet, inches = parts
    return int(int(feet) * 30.48 + int(inches[:-1]) * 2.54)


def parse_profile_page(url):
    r = requests.get(url)
    tree = BeautifulSoup(r.text, 'html.parser')
    sections = tree.select('#wrapper div.maincontainer main section.sectionspace')
    if not sections:
        raise ValueError('Account deleted or not activated')

    profile_container = sections[0]
    first_dts = profile_container.select('div.row:nth-of-type(1) dt')
    values = [dt.text.strip() for dt in first_dts]

    second_values = [dt.text for boxes in tree.select('div.whitelinebox.responsive_block')[2:] for dt in boxes.select('dt')]

    profile = date_profile.Profile()
    profile.url = url
    profile.gender = values[0]
    profile.country = values[1]
    profile.city = values[2]
    profile.state = values[3]
    profile.height_cm = get_height_cm(values[4])
    profile.age = int(values[6])
    profile.eye_color = values[7]
    profile.body_type = values[8]
    profile.hair_color = values[9]
    profile.ethnicity = values[10]
    profile.denomination = values[11]
    profile.photo_urls = '|'.join([img['src'] for img in tree.select('div.tooltip-img img')])
    profile.looking_for = second_values[0]
    profile.church_name = second_values[1]
    profile.church_attendance = second_values[2]
    profile.church_raised_in = second_values[3]
    profile.drink = second_values[4]
    profile.smoke = second_values[5]
    profile.willing_to_relocate = second_values[6]
    profile.marital_status = second_values[7]
    profile.have_children = second_values[8] == 'Yes'
    profile.want_children = second_values[9]
    profile.education_level = second_values[10]
    profile.profession = second_values[11]

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


def get_profile_links(search_url, search_params={}):

    url_params = get_url_params(search_params)
    start = 0
    while True:
        url_params['start'] = start
        r = requests.get(search_url, url_params)
        tree = BeautifulSoup(r.text, 'html.parser')
        prof_boxes = tree.select('div.user-grid-list.clearfix.clear_margin article')
        if not prof_boxes:
            break

        for art in prof_boxes:
            yield art.a['href']

        start += 12


def get_countries():
    r = requests.get('https://www.christiandatingforfree.com/basic_search.php?'
                     'u_seeking=Female&age_from=18&age_to=26&u_looking_for_value=0&'
                     'u_country=30&u_state=&u_city=&u_postalcode=&distance=&dest=&'
                     'Submit=Submit')

    tree = BeautifulSoup(r.text, 'html.parser')
    return {opt['value']: opt.text for opt in tree.select('#u_country option')}
