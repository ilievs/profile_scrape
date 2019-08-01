import urllib.parse

from werkzeug.exceptions import BadRequest
from flask import Flask, request, render_template

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker

from model.profile import *
from collections import OrderedDict


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

engine = create_engine('mysql+mysqlconnector://moblytics:moblytics@192.168.68.128:3306/moblytics', echo=False)
DbSession = sessionmaker(bind=engine)
db_session = DbSession()


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


def get_search_criteria_meta():

    search_criteria_meta = OrderedDict()
    search_criteria_meta['']
    Profile.__table__.columns
    for c in Profile.__table__.columns:
        field_criteria_meta = {
            'type': c.type.__visit_name__
        }

        try:
            field_criteria_meta['validValues'] = [m for m in c.type.python_type.__members__]
        except AttributeError:
            pass

        search_criteria_meta[c.name] = field_criteria_meta

    search_criteria_meta['keywords'] = {
        'type': 'text'
    }

    return search_criteria_meta


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
def get_home():
    return render_template('home.html')


def get_query(db_session, search_criteria):

    db_criteria = []

    try:

        genders = search_criteria.get('gender')
        if genders:
            db_criteria.append(Profile.gender == genders)

        country = search_criteria.get('country')
        if country:
            db_criteria.append(Profile.country == country)

        age_from = search_criteria.getlist('ageFrom', int)
        if age_from:
            db_criteria.append(Profile.age >= age_from[0])

        age_to = search_criteria.getlist('ageTo', int)
        if age_to:
            db_criteria.append(Profile.age <= age_to[0])

        height_from = search_criteria.getlist('heightFrom', int)
        if height_from:
            db_criteria.append(Profile.height_cm >= height_from[0])

        height_to = search_criteria.getlist('heightTo', int)
        if height_to:
            db_criteria.append(Profile.height_cm <= height_to[0])

        keywords = search_criteria.get('keywords')
        if keywords:
            conditions = [con for k in keywords.split(',')
                          for con in [Profile.profession.contains(k),
                                      Profile.interests.contains(k),
                                      Profile.about_me.contains(k),
                                      Profile.first_date.contains(k)]]

            db_criteria.append(or_(*conditions))

        church_attendance = search_criteria.get('churchAttendance')
        if church_attendance:
            db_criteria.append(Profile.church_attendance == church_attendance)

        looking_for_values = search_criteria.getlist('lookingFor', LookingFor)
        if looking_for_values:
            db_criteria.append(Profile.looking_for.in_(looking_for_values))

        drink_values = search_criteria.getlist('drink', Drink)
        if drink_values:
            db_criteria.append(Profile.drink.in_(drink_values))

        smoke_values = search_criteria.getlist('smoke', Smoke)
        if smoke_values:
            db_criteria.append(Profile.smoke.in_(smoke_values))

        body_types = search_criteria.getlist('bodyType', BodyType)
        if body_types:
            db_criteria.append(Profile.body_type.in_(body_types))

        denominations = search_criteria.getlist('denomination', Denomination)
        if denominations:
            db_criteria.append(Profile.denomination.in_(denominations))

        education_levels = search_criteria.getlist('educationLevel', EducationLevel)
        if education_levels:
            db_criteria.append(Profile.education_level.in_(education_levels))

        ethnicity_values = search_criteria.getlist('ethnicity', Ethnicity)
        if ethnicity_values:
            db_criteria.append(Profile.ethnicity.in_(ethnicity_values))

        hair_colors = search_criteria.getlist('hairColor', HairColor)
        if hair_colors:
            db_criteria.append(Profile.hair_color.in_(hair_colors))

        eye_colors = search_criteria.getlist('eyeColor', EyeColor)
        if eye_colors:
            db_criteria.append(Profile.eye_color.in_(eye_colors))

        marital_status = search_criteria.getlist('maritalStatus', MaritalStatus)
        if marital_status:
            db_criteria.append(Profile.marital_status.in_(marital_status))

        user_wants_children = search_criteria.getlist('userWantsChildren', UserWantsChildren)
        if user_wants_children:
            db_criteria.append(Profile.want_children.in_(user_wants_children))

        user_with_children = search_criteria.getlist('userWithChildren', UserWithChildren)
        if user_with_children:
            db_criteria.append(Profile.have_children.in_(user_with_children))

        if search_criteria.get('onlyWithPhotos', None):
            db_criteria.append(Profile.photo_urls != '')

    except ValueError:
        pass

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

    results = get_query(db_session, request.args)[start:end]

    for r in results:
        r.photo_urls_list = r.photo_urls.split('|')

    prev_link, next_link = get_pagination_links(request.url, start, size)

    return render_template('profiles.html',
                           profiles=results,
                           start=start,
                           size=size,
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

    # profile_dicts = [r.as_dict() for r in results]
    #
    # try:
    #     for pd in profile_dicts:
    #         pd['photo_urls'] = pd['photo_urls'].split('|')
    # except LookupError:
    #     pass
    #
    # return json.jsonify(profile_dicts)


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