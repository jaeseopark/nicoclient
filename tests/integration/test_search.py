import unittest

from nicoclient import search_daily_trending_utatttemita_videos
from nicoclient.core import search


class TestSearch(unittest.TestCase):
    def test_related_videos_vocaloid_org(self):
        videos = search.search_utattemita_videos('sm32076378')
        self.assertTrue(len(videos) > 1)

    def test_get_trending_videos(self):
        videos = search_daily_trending_utatttemita_videos(min_likes=25)
        self.assertGreater(len(videos), 0)
        for video in videos:
            with self.subTest(video_id=video.id):
                self.assertGreater(video.likes, 25)
