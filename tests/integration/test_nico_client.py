import unittest

from nico_client import get_daily_trending_videos, get_related_videos, populate_details
from nico_client.model.video import Video


@unittest.skip("Skipping integration tests by default")
class TestNicoClient(unittest.TestCase):
    def test_get_daily_trending_videos(self):
        videos = get_daily_trending_videos()
        self.assertEqual(100, len(videos))
        for video in videos:
            with self.subTest(video_id=video.id, views=video.views, likes=video.likes):
                self.assertIsNotNone(video.id, 'id should not be None')
                self.assertTrue(video.views > 0, 'video.views must be greater than 0')

    def test_related_videos(self):
        for video_id in ['sm34775615', 'sm34734479']:
            with self.subTest(video_id=video_id):
                video = Video(id=video_id)
                videos = get_related_videos(video)
                self.assertTrue(len(videos) > 1)

    def test_video_attribute_population(self):
        video = Video(id='sm34734479')
        self.assertIsNone(video.views)
        populate_details(video)
        self.assertEqual(type(video.views), int, "video.views is expected to be an integer")
