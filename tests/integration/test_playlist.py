from nico_client.html_page.playlist import Playlist
from tests import IntegrationTest


class TestPlaylist(IntegrationTest):
    def test_get_videos(self):
        p = Playlist(id='19160554')
        p.get_videos()
