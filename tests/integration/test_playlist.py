import unittest

from nico_client.html_page.playlist import Playlist


class TestPlaylist(unittest.TestCase):
    def test_get_videos(self):
        p = Playlist(id='19160554')
        videos = p.get_videos()
        self.assertGreater(len(videos), 0)
