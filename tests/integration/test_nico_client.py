import unittest

from nico_client.client import NicoClient


class TestNicoClient(unittest.TestCase):
    def test_get_daily_trending_videos(self):
        client = NicoClient()
        videos = client.get_daily_trending_videos()
