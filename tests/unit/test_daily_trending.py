from nico_client.html_page.trending import Trending
from tests import UnitTest


class TestDailyTrending(UnitTest):
    def test_video_conversion(self):
        html_str = self.get_file_content_as_string('daily_trending.html')
        dt = Trending(html_string=html_str, new_videos_only=False)
        videos = dt.get_videos()
        self.assertEqual(100, len(videos))
        for video in videos:
            with self.subTest(video_id=video.id):
                self.assertIsNotNone(video.id, 'id should not be None')
                self.assertTrue(video.views > 0, 'video.views must be greater than 0')
                self.assertTrue(video.likes > 0, 'video.likes must be greater than 0')
