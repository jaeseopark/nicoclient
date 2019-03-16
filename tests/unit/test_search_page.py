from nico_client.html_page.search_page import UtattemitaSearchPage
from tests import UnitTest


class TestUtattemitaSearchPage(UnitTest):
    def test_get_videos(self):
        html_string = self.get_file_content_as_string('search_1.html')
        search_page = UtattemitaSearchPage(html_string=html_string)
        videos = search_page.get_videos()
        self.assertEqual(len(videos), 9)
