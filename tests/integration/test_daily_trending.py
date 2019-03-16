from nico_client import get_daily_trending_videos
from tests import IntegrationTest


class TestDailyTrending(IntegrationTest):
    def test_get_daily_trending_videos(self):
        videos = get_daily_trending_videos()
        self.assertEqual(100, len(videos))
        for video in videos:
            with self.subTest(video_id=video.id, views=video.views, likes=video.likes):
                self.assertIsNotNone(video.id, 'id should not be None')
                self.assertTrue(video.views > 0, 'video.views must be greater than 0')
