import unittest

from nico_client.html_page.trending import Trending, get_trending_videos


class TestDailyTrending(unittest.TestCase):
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

    def test_get_trending_videos_with_min_likes(self):
        videos1 = get_trending_videos('daily')
        videos2 = get_trending_videos('daily', min_likes=100)
        self.assertGreater(len(videos1), len(videos2))
