import os
from urllib.parse import urlparse

import bs4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import requests

from model.profile import *


def get_user_id(url):
    u = urlparse(url)
    return {pair.split('=')[0]: pair.split('=')[1] for pair in u.query.split('&')}.get('userid')


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


def remove_duplicates():

    engine = create_engine('mysql+mysqlconnector://moblytics:moblytics@192.168.68.128:3306/moblytics', echo=False)
    Base.metadata.create_all(engine)
    DbSession = sessionmaker(bind=engine)
    db_session = DbSession()

    step = 1000
    fr = 0
    to = step

    profile_ids = set()
    duplicates_ids = []
    while True:
        users = db_session.query(Profile).order_by(Profile.id)[fr:to]
        if not users:
            break
        for u in users:
            uid = int(get_user_id(u.url))
            if uid in profile_ids:
                duplicates_ids.append(u.id)
                if len(duplicates_ids) % 100 == 0:
                    print('Removing', len(duplicates_ids), 'duplicates')
                    stmt = Profile.__table__.delete().where(Profile.id.in_(duplicates_ids))
                    db_session.execute(stmt)
                    db_session.commit()
                    duplicates_ids = []
            else:
                profile_ids.add(uid)



        fr += step
        to += step


def is_account_activated(url, params={}):
    r = requests.get(url, params=params)
    tree = bs4.BeautifulSoup(r.text, 'html.parser')

    alerts = tree.select('div.alert.alert-danger')
    for a in alerts:
        if a.text.strip() == 'This user profile has not yet been activated by CDFF.':
            return False

    return True
