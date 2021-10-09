import unittest

from com.dreamlab.profile_scrape.parser.profile import ProfilePageParser
from model.profile import *


class TestProfileScrape(unittest.TestCase):

    def test_normal_profile(self):

        page_parser = ProfilePageParser()

        html_file_dir = '/'.join(__file__.split('/')[:-1]) + '/example_profile.html'
        with open(html_file_dir, 'rt', encoding='utf-8') as f:
            profile = page_parser.parse(f.read())

            self.assertEqual('https://www.christiandatingforfree.com/view_profile.php?userid=3240819&pind=2',
                             profile.url)

            self.assertEqual(Gender.female, profile.gender)
            self.assertEqual("United States", profile.country)
            self.assertEqual("Detroit", profile.city)
            self.assertEqual("Michigan", profile.state)
            self.assertEqual(162, profile.height)
            self.assertEqual(23, profile.age)
            self.assertEqual(EyeColor.brown, profile.eye_color)
            self.assertEqual(BodyType.slender, profile.body_type)
            self.assertEqual(HairColor.black, profile.hair_color)
            self.assertEqual(Ethnicity.africanAmerican, profile.ethnicity)
            self.assertEqual(Denomination.christianReformed, profile.denomination)
            self.assertEqual('https://photos.christiandatingforfree.com/thumb_cache/2020/0815/480x/'
                             'u_id_3240819__480x480__width_height__20200815171833__%28%7C%29usr%4032'
                             '40819%402020-08-15%28%7C%290bcd9bb5ce0653afba556eb5faf17287.jpg|'
                             
                             'https://photos.christiandatingforfree.com/thumb_cache/2020/0815/480x/'
                             'u_id_3240819__480x480__width_height__20200815172314__%28%7C%29usr%4032'
                             '40819%402020-08-15%28%7C%29d011e030bc75724e8433c34df71d5d78.jpg|'
                             
                             'https://photos.christiandatingforfree.com/thumb_cache/2020/0815/480x/'
                             'u_id_3240819__480x480__width_height__20200815172434__%28%7C%29usr%4032'
                             '40819%402020-08-15%28%7C%29a97a2ee88342986010dd87ebb042a9be.jpg|'
                             
                             'https://photos.christiandatingforfree.com/thumb_cache/2020/0815/480x/'
                             'u_id_3240819__480x480__width_height__20200906230117__%28%7C%29usr%4032'
                             '40819%402020-08-15%28%7C%292ae48956703c5984f5b8fa480ab5dca8.jpg|'
                             
                             'https://photos.christiandatingforfree.com/thumb_cache/2020/0815/480x/'
                             'u_id_3240819__480x480__width_height__20200906230153__%28%7C%29usr%4032'
                             '40819%402020-08-15%28%7C%2960b850c08a77b98c4b6e6899888f093f.jpg',

                             profile.image_urls)

            self.assertEqual(LookingFor.longTermRelationship, profile.looking_for)
            self.assertEqual('Word Of Faith international Christian center', profile.church_name)
            self.assertEqual(ChurchAttendance.everyWeek, profile.church_attendance)
            self.assertEqual('', profile.church_raised_in)
            self.assertEqual(Drink.no, profile.drink)
            self.assertEqual(Smoke.no, profile.smoke)
            self.assertEqual(WillingToRelocate.sureWhyNot, profile.willing_to_relocate)
            self.assertEqual(MaritalStatus.single, profile.marital_status)
            self.assertEqual(UserWithChildren.yes, profile.have_children)
            self.assertEqual(UserWantsChildren.wantChildren, profile.want_children)
            self.assertEqual(EducationLevel.highSchoolGraduate, profile.education_level)
            self.assertEqual('Helping People Get Closer God', profile.profession)
            self.assertEqual('Men', profile.interests)
            self.assertEqual("I'm a God-fearing woman that's loving caring and love helping people 😁💖💯",
                             profile.about_me)

            self.assertEqual('Take long walks by the beach or River', profile.first_date)
            self.assertEqual('Age between 22 to 28.|'
                             'Must not Smoke.|'
                             'Must not Drink.|'
                             'Appears on 11 members favorites lists',
                             profile.account_settings_criteria)
