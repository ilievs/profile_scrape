import logging
import traceback

import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.entity_base import Base

from scrape import profile_scrape


if __name__ == '__main__':

    logging.basicConfig(filename='log.txt',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    logging.info("Starting SQL engine")

    logger = logging.getLogger('profile_scrape')

    engine = create_engine('mysql+mysqlconnector://moblytics:moblytics@192.168.68.128:3306/moblytics', echo=False)
    Base.metadata.create_all(engine)
    DbSession = sessionmaker(bind=engine)
    db_session = DbSession()

    photos_path = 'photos/'

    logger.info('Links to failed profile scraping:')

    countries = profile_scrape.get_countries()
    for seeking in ['female', 'male']:
        for country in countries:
            search_params = {
                'seeking': seeking,
                'fromAge': 18,
                'toAge': 99,
                'country': country,
            }

            links = profile_scrape.get_profile_links('https://www.christiandatingforfree.com/basic_search.php', search_params)

            for l in links:
                try:
                    r = requests.get(l)
                    profile = profile_scrape.parse_profile_page(l, r.text)
                    #profile_scrape.download_photos(profile, photos_path)

                    db_session.add(profile)
                    db_session.commit()

                except Exception as e:
                    traceback.print_exc()
                    logger.error(traceback.format_stack())
                    logger.error(l)
                    print('Something went wrong: ', e)
                    print('Link to profile: ', l)

    logging.shutdown()
