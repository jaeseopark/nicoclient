import unittest

from nicoclient.html_page.search_page import UtattemitaSearchPage
from tests import get_file_content_as_string


class TestUtattemitaSearchPage(unittest.TestCase):
    def test_get_videos(self):
        html_string = get_file_content_as_string('search_1.html')
        search_page = UtattemitaSearchPage(html_string=html_string)
        videos = search_page.get_videos()
        self.assertEqual(len(videos), 9)
