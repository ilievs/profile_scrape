import unittest

from scrape.profile_scrape import parse_profile_page


class ProfileScrapeTest(unittest.TestCase):

    def test_normal_profile(self):
        with open('scrape/example_profile.html', 'rt', encoding='utf-8') as f:
            url = 'https://www.christiandatingforfree.com/view_profile.php?userid=2379593&pind=0'
            profile = parse_profile_page(url, f.read())

            self.assertEqual(profile.gender, "Female")
            self.assertEqual(profile.country, "Brazil")
            self.assertEqual(profile.city, "Cuiabá")
            self.assertEqual(profile.state, "Mato Grosso")
            self.assertEqual(profile.height_cm, 162)
            self.assertEqual(profile.age, 21)
            self.assertEqual(profile.eye_color, 'Brown')
            self.assertEqual(profile.body_type, 'Athletic')
            self.assertEqual(profile.hair_color, 'Brown')
            self.assertEqual(profile.ethnicity, 'Prefer not to say')
            self.assertEqual(profile.denomination, 'Evangelical')
            self.assertEqual(profile.photo_urls, 'http://photos.christiandatingforfree.com/thumb_cache/2019/0302/480x/'
                                                 'u_id_2379593__480x480__width_height__20190304041453__%28%7C%29usr%402'
                                                 '379593%402019-03-02%28%7C%29f375873dc3ce9e704e110a8c72e3569c.jpg|'
                                                 'http://photos.christiandatingforfree.com/thumb_cache/2019/0302/480x/'
                                                 'u_id_2379593__480x480__width_height__20190525200334__%28%7C%29usr%40'
                                                 '2379593%402019-03-02%28%7C%2955d4d6cc1c8a9b0fe9c5396f3caee4e7.jpg|'
                                                 'http://photos.christiandatingforfree.com/thumb_cache/2019/0302/480x/'
                                                 'u_id_2379593__480x480__width_height__20190525200503__%28%7C%29usr%40'
                                                 '2379593%402019-03-02%28%7C%298d2ec5fbf920e32201a18e6f5572b04c.jpg')
            self.assertEqual(profile.looking_for, 'A Long Term Relationship')
            self.assertEqual(profile.church_name, 'Congregação')
            self.assertEqual(profile.church_attendance, 'Every week')
            self.assertEqual(profile.church_raised_in, 'Evangelical')
            self.assertEqual(profile.drink, 'No')
            self.assertEqual(profile.smoke, 'No')
            self.assertEqual(profile.willing_to_relocate, 'Possibly, who knows')
            self.assertEqual(profile.marital_status, 'Single')
            self.assertEqual(profile.have_children, 'No')
            self.assertEqual(profile.want_children, 'Undecided/Open')
            self.assertEqual(profile.education_level, 'HS Graduate')
            self.assertEqual(profile.profession, 'Biomedicina')
            self.assertEqual(profile.interests, None)
            self.assertEqual(profile.about_me, "I'm Amandha, I like to practice gym, I'm a college student Biomedical,"
                                               " I love in my book, I like to be with my Family, to go to the park.")
            self.assertEqual(profile.first_date, None)
            self.assertEqual(profile.account_settings_criteria, 'Any Age.')
