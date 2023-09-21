import unittest

from nicoclient.html_page.html_page import HtmlPage
from nicoclient.html_page.playlist import Playlist, PlaylistPage
from tests import get_file_content_as_string


class PlaylistPageWithHtmlInjection(PlaylistPage):
    def __init__(self, html_string: str):
        HtmlPage.__init__(self, html_string=html_string)
        self.id = "foobar"
        self._parse()


class TestPlaylist(unittest.TestCase):
    def test_get_videos_preload(self):
        raw_html = get_file_content_as_string('mylist.html')
        plpage = PlaylistPageWithHtmlInjection(html_string=raw_html)
        videos = plpage.playlist.videos
        self.assertTrue(len(videos) > 0)
        for video in videos:
            with self.subTest(video_id=video.id):
                self.assertEqual(int, type(video.views))

    def test_get_videos_wo_preload(self):
        raw_html = get_file_content_as_string('mylist_without_preload.html')
        plpage = PlaylistPageWithHtmlInjection(html_string=raw_html)
        videos = plpage.playlist.videos
        self.assertTrue(len(videos) > 0)
        for video in videos:
            with self.subTest(video_id=video.id):
                self.assertEqual(int, type(video.views))

    def test_get_owner_id(self):
        raw_html = get_file_content_as_string('mylist.html')
        plpage = PlaylistPageWithHtmlInjection(html_string=raw_html)
        owner_id = plpage.playlist.owner_id
        self.assertEqual('52479273', owner_id)
