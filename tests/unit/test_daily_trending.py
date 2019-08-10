import unittest

from nicoclient.html_page.trending import Trending
from tests import get_file_content_as_string


class TestDailyTrending(unittest.TestCase):
    def test_video_conversion(self):
        html_str = get_file_content_as_string('daily_trending.html')
        dt = Trending(html_string=html_str, new_videos_only=False)
        videos = dt.get_videos()
        self.assertEqual(100, len(videos))
        for video in videos:
            with self.subTest(video_id=video['id']):
                self.assertIsNotNone(video.get('id'), 'id should not be None')
                self.assertIsNotNone(video.get('title'), 'title should not be None')
                self.assertGreater(video.get('upload_time'), 0, 'upload_titme must be greater than 0')
                self.assertGreater(video.get('views'), 0, 'views must be greater than 0')
                self.assertGreater(video.get('likes'), 0, 'likes must be greater than 0')

    def test_video_age(self):
        html_str = get_file_content_as_string('daily_trending.html')
        dt1 = Trending(html_string=html_str, new_videos_only=True)
        dt2 = Trending(html_string=html_str, new_videos_only=False)

        len1 = len(dt1.get_videos())
        len2 = len(dt2.get_videos())
        self.assertGreater(len2, len1, "more videos should be returned when new_videos_only=False")
