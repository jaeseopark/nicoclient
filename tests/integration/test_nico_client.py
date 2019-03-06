import unittest

from nico_client.client import NicoClient


class TestNicoClient(unittest.TestCase):
    def test_get_daily_trending_videos(self):
        client = NicoClient()
        videos = client.get_daily_trending_videos()
        for video in videos:
            self.assertIsNotNone(video.id, 'id should not be None')
            self.assertTrue(video.views > 0, 'video.views must be greater than 0')
            self.assertTrue(video.likes > 0, 'video.likes must be greater than 0')