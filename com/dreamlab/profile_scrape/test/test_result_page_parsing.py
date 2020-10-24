import unittest

from scrape.profile_scrape import get_profile_links


class TestResultPageParsing(unittest.TestCase):

    def test_normal_profile(self):
        with open('com/dreamlab/profile_scrape/test/example_results_page.html', 'rt', encoding='utf-8') as f:

            links = get_profile_links(f.read())

            self.assertEqual(links, ['https://www.christiandatingforfree.com/view_profile.php?userid=1870550&pind=',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=2460464&pind=1',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=2452997&pind=2',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=2506925&pind=3',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=2612099&pind=0',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=2382029&pind=1',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=2604596&pind=2',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=2601052&pind=3',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=1933953&pind=4',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=2578331&pind=5',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=2191801&pind=6',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=2612248&pind=7',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=1064305&pind=8',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=2518835&pind=9',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=2563073&pind=10',
                                    'https://www.christiandatingforfree.com/view_profile.php?userid=1638539&pind=11'])