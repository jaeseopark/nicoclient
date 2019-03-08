import unittest

from nico_client.client import NicoClient
from nico_client.video import Video


@unittest.skip("Skipping integration tests by default")
class TestNicoClient(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.client = NicoClient()

    def test_get_daily_trending_videos(self):
        videos = self.client.get_daily_trending_videos()
        for video in videos:
            self.assertIsNotNone(video.id, 'id should not be None')
            self.assertTrue(video.views > 0, 'video.views must be greater than 0')
            self.assertTrue(video.likes > 0, 'video.likes must be greater than 0')

    def test_related_videos(self):
        videos = self.client.get_related_videos(Video(id='sm34734479'))
        self.assertTrue(len(videos) > 1)

    def test_video_attribute_population(self):
        video = Video(id='sm34734479')
        self.client.populate_details(video)
        self.assertEqual(type(video.views), int, "video.views is expected to be an integer")
