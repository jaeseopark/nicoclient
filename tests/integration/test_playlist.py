import unittest

from nicoclient.html_page.playlist import PlaylistPage


class TestPlaylist(unittest.TestCase):
    def test_get_videos(self):
        plpage = PlaylistPage(id='19160554')
        self.assertGreater(len(plpage.playlist.videos), 0)
