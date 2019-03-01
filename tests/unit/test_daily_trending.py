import unittest

from nico_client.html_page.daily_trending import DailyTrending
from tests.helper import get_file_content_as_string


class TestDailyTrending(unittest.TestCase):
    def test_video_conversion(self):
        html_str = get_file_content_as_string('daily_trending.html')
        dt = DailyTrending(html_str)
        videos = dt.get_videos()
        self.assertEqual(100, len(videos))
        for video in videos:
            self.assertIsNotNone(video.video_id, 'video_id should not be None')
            self.assertTrue(video.views > 0, 'video.views must be greater than 0')
            self.assertTrue(video.likes > 0, 'video.likes must be greater than 0')