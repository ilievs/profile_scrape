import urllib.parse
import os
import subprocess
import json

from werkzeug.exceptions import BadRequest
from flask import Flask, request, render_template

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, Bundle

from model.profile import *
from collections import OrderedDict

from common.config import read_config

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

config = read_config()

engine = create_engine(config.db_url, echo=False)
DbSession = sessionmaker(bind=engine)
db_session = DbSession()


def start_server():
    os.environ['FLASK_APP'] = 'web.controller.profile_controller.py'
    subprocess.run(['python', '-m', 'flask', 'run'])


def uncamel(string):

    if string:
        new_str = ''.join(map(lambda c: c if c.islower() else ' ' + c, string))
        return new_str.capitalize()

    return None


gender_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(Gender) if lf.name != 'undefined'}
looking_for_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(LookingFor) if lf.name != 'undefined'}
church_attendance_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(ChurchAttendance) if lf.name != 'undefined'}
drink_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(Drink) if lf.name != 'undefined'}
smoke_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(Smoke) if lf.name != 'undefined'}
body_type_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(BodyType) if lf.name != 'undefined'}
denomination_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(Denomination) if lf.name != 'undefined'}
education_level_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(EducationLevel) if lf.name != 'undefined'}
marital_status_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(MaritalStatus) if lf.name != 'undefined'}
ethnicity_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(Ethnicity) if lf.name != 'undefined'}
hair_color_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(HairColor) if lf.name != 'undefined'}
eye_color_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(EyeColor) if lf.name != 'undefined'}
user_wants_children_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(UserWantsChildren) if lf.name != 'undefined'}
user_with_children_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(UserWithChildren) if lf.name != 'undefined'}
willing_to_relocate_name_to_display_name = {lf.name: uncamel(lf.name) for lf in list(WillingToRelocate) if lf.name != 'undefined'}


def get_pagination_links(url, start, size):
    url_parts = urllib.parse.urlparse(url)

    if url_parts.query:
        query_params = urllib.parse.parse_qs(url_parts.query)
    else:
        query_params = {}

    # for the prev page
    prev_link = None
    if start > 0:
        query_params['start'] = max(0, start - size)
        prev_link = url_parts.path + '?' + urllib.parse.urlencode(query_params, doseq=True)
    elif 'start' in query_params:
        del query_params['start']

    # in case the query is missing the pagination params
    query_params['size'] = size

    query_params['start'] = start + size
    next_link = url_parts.path + '?' + urllib.parse.urlencode(query_params, doseq=True)

    return prev_link, next_link


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def get_home():
    return render_template('home.html')


url_param_to_db_criteria = {
    'gender': lambda gender: Profile.gender == Gender[gender[0]],
    'country': lambda country: Profile.country == country[0],
    'ageFrom': lambda age_from: Profile.age >= int(age_from[0]),
    'ageTo': lambda age_to: Profile.age <= int(age_to[0]),
    'heightFrom': lambda height_from: Profile.height_cm >= int(height_from[0]),
    'heightTo': lambda height_to: Profile.height_cm <= int(height_to[0]),
    'keywords': lambda keywords: or_(*[con for k in keywords[0].split(',')
                                       for con in [Profile.profession.contains(k),
                                                   Profile.interests.contains(k),
                                                   Profile.about_me.contains(k),
                                                   Profile.first_date.contains(k)]]),

    'churchAttendance': lambda attendance_list: Profile.church_attendance == ChurchAttendance[attendance_list[0]],
    'lookingFor': lambda looking_for_values: Profile.looking_for.in_([LookingFor[l] for l in looking_for_values]),
    'drink': lambda drink_values: Profile.drink.in_([Drink[v] for v in drink_values]),
    'smoke': lambda smoke_values: Profile.smoke.in_([Smoke[v] for v in smoke_values]),
    'bodyType': lambda body_types: Profile.body_type.in_([BodyType[v] for v in body_types]),
    'denomination': lambda denominations: Profile.denomination.in_([Denomination[v] for v in denominations]),
    'educationLevel':
        lambda education_levels: Profile.education_level.in_([EducationLevel[v] for v in education_levels]),

    'ethnicity': lambda ethnicity_values: Profile.ethnicity.in_([Ethnicity[v] for v in ethnicity_values]),
    'hairColor': lambda hair_colors: Profile.hair_color.in_([HairColor[v] for v in hair_colors]),
    'eyeColor': lambda eye_colors: Profile.eye_color.in_([EyeColor[v] for v in eye_colors]),
    'maritalStatus': lambda marital_status: Profile.marital_status.in_([MaritalStatus[v] for v in marital_status]),
    'userWantsChildren':
        lambda user_wants_children: Profile.want_children.in_([UserWantsChildren[v] for v in user_wants_children]),

    'userWithChildren':
        lambda user_with_children: Profile.have_children.in_([UserWithChildren[v] for v in user_with_children]),

    'onlyWithPhotos': lambda only_with_photos: Profile.photo_urls != '' if only_with_photos[0] else None,
}


def get_query(db_session, search_criteria):

    db_criteria = []

    try:
        for param_name, handler in url_param_to_db_criteria.items():
            param_value = search_criteria.getlist(param_name)
            if param_value:
                db_criteria.append(handler(param_value))

    except (ValueError, KeyError, TypeError):
        raise BadRequest('Wrong param name or value detected')

    query = db_session.query(Profile)

    if db_criteria:
        query = query.filter(*db_criteria)

    return query


def get_start_size(request):
    try:
        start = int(request.args.get('start'))
        size = int(request.args.get('size'))

        if start < 0 or size < 1 or size > 100:
            raise ValueError()

        return start, size

    except (ValueError, TypeError):
        return 0, 30


@app.route('/profiles', methods=['GET'])
def get_profiles():

    start, size = get_start_size(request)

    end = start + size

    query = get_query(db_session, request.args)
    total = query.count()
    results = query[start:end]

    for r in results:
        r.photo_urls_list = r.photo_urls.split('|')

    prev_link, next_link = get_pagination_links(request.url, start, size)

    return render_template('profiles.html',
                           profiles=results,
                           start=start,
                           size=size,
                           total=total,
                           prev_page_link=prev_link,
                           next_page_link=next_link,
                           gender_name_to_display_name=gender_name_to_display_name,
                           looking_for_name_to_display_name=looking_for_name_to_display_name,
                           church_attendance_name_to_display_name=church_attendance_name_to_display_name,
                           drink_name_to_display_name=drink_name_to_display_name,
                           smoke_name_to_display_name=smoke_name_to_display_name,
                           body_type_name_to_display_name=body_type_name_to_display_name,
                           denomination_name_to_display_name=denomination_name_to_display_name,
                           education_level_name_to_display_name=education_level_name_to_display_name,
                           marital_status_name_to_display_name=marital_status_name_to_display_name,
                           ethnicity_name_to_display_name=ethnicity_name_to_display_name,
                           hair_color_name_to_display_name=hair_color_name_to_display_name,
                           eye_color_name_to_display_name=eye_color_name_to_display_name,
                           user_wants_children_name_to_display_name=user_wants_children_name_to_display_name,
                           user_with_children_name_to_display_name=user_with_children_name_to_display_name,
                           willing_to_relocate_name_to_display_name=willing_to_relocate_name_to_display_name,
                           search_criteria=request.args)


@app.route('/view_profile', methods=['GET'])
def view_profile():
    try:
        id = int(request.args.get('id'))
    except ValueError:
        raise BadRequest('invalid id')

    profile = db_session.query(Profile).get(id)
    if not profile:
        raise BadRequest('Could not find profile with given id')

    profile.photo_urls_list = profile.photo_urls.split('|')

    return render_template('view_profile.html', profile=profile)


@app.route('/analytics_profiles', methods=['GET'])
def get_all_profiles():

    class DictBundle(Bundle):
        def create_row_processor(self, query, procs, labels):
            """Override create_row_processor to return values as dictionaries"""

            def proc(row):
                return dict(
                    zip(labels, (proc(row) for proc in procs))
                )

            return proc

    bn = DictBundle('bundle', Profile.gender,
                    Profile.country,
                    Profile.city,
                    Profile.state,
                    Profile.height_cm,
                    Profile.age,
                    Profile.eye_color,
                    Profile.hair_color,
                    Profile.body_type,
                    Profile.ethnicity,
                    Profile.denomination,
                    Profile.looking_for,
                    Profile.church_name,
                    Profile.church_attendance,
                    Profile.church_raised_in,
                    Profile.drink,
                    Profile.smoke,
                    Profile.willing_to_relocate,
                    Profile.marital_status,
                    Profile.have_children,
                    Profile.want_children,
                    Profile.education_level,
                    Profile.profession)

    profiles = db_session.query(bn)

    return json.dumps([p.bundle for p in profiles])


@app.route('/analytics', methods=['GET'])
def analytics_page():
    return render_template('analytics.html')