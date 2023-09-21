import unittest

from nicoclient.html_page.playlist import Playlist


class TestPlaylist(unittest.TestCase):
    def test_get_videos(self):
        p = Playlist(id='19160554')
        self.assertGreater(len(p.videos), 0)
