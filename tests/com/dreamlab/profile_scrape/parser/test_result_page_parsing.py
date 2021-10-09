import unittest

from scrape.profile_scrape import get_profile_links


class TestResultPageParsing(unittest.TestCase):

    def test_normal_profile(self):
        html_file_dir = '/'.join(__file__.split('/')[:-1]) + '/example_results_page.html'
        with open(html_file_dir, 'rt', encoding='utf-8') as f:

            links = get_profile_links(f.read())

            self.assertEqual(links, [
                'https://www.christiandatingforfree.com/view_profile.php?userid=3281189&pind=',
                'https://www.christiandatingforfree.com/view_profile.php?userid=3129887&pind=1',
                'https://www.christiandatingforfree.com/view_profile.php?userid=3240819&pind=2',
                'https://www.christiandatingforfree.com/view_profile.php?userid=3205163&pind=3',
                'https://www.christiandatingforfree.com/view_profile.php?userid=3295921&pind=0',
                'https://www.christiandatingforfree.com/view_profile.php?userid=3177033&pind=1',
                'https://www.christiandatingforfree.com/view_profile.php?userid=3321665&pind=2',
                'https://www.christiandatingforfree.com/view_profile.php?userid=3316820&pind=3',
                'https://www.christiandatingforfree.com/view_profile.php?userid=3313726&pind=4',
                'https://www.christiandatingforfree.com/view_profile.php?userid=3321659&pind=5',
                'https://www.christiandatingforfree.com/view_profile.php?userid=3283893&pind=6',
                'https://www.christiandatingforfree.com/view_profile.php?userid=2666629&pind=7',
                'https://www.christiandatingforfree.com/view_profile.php?userid=3321704&pind=8',
                'https://www.christiandatingforfree.com/view_profile.php?userid=3317072&pind=9',
                'https://www.christiandatingforfree.com/view_profile.php?userid=3318423&pind=10',
                'https://www.christiandatingforfree.com/view_profile.php?userid=1481997&pind=11',
            ])
