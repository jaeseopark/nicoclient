from nico_client.html_page.trending import Trending
from tests import IntegrationTest


class TestDailyTrending(IntegrationTest):
    def test_get_trending_videos_all(self):
        for time_range in ['daily', 'weekly']:
            with self.subTest(time_range=time_range):
                videos = Trending(time_range, new_videos_only=False).get_videos()
                self.assertEqual(100, len(videos))

    def test_get_trending_videos_new_videos_only(self):
        for time_range in ['daily', 'weekly']:
            with self.subTest(time_range=time_range):
                videos = Trending(time_range).get_videos()
                self.assertGreater(len(videos), 0)
