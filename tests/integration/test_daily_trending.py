from nico_client.html_page.trending import Trending
from tests import IntegrationTest


class TestDailyTrending(IntegrationTest):
    def test_get_daily_trending_videos(self):
        videos = Trending('daily', new_videos_only=False).get_videos()
        self.assertEqual(100, len(videos))
        for video in videos:
            with self.subTest(video_id=video.id, views=video.views, likes=video.likes):
                self.assertIsNotNone(video.id)
                self.assertGreater(video.views, 0)
