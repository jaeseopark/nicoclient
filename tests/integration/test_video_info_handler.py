import unittest

from nicoclient.core.lookup import get_video_by_id


class TestVideoInfoHandler(unittest.TestCase):
    def test_video_attribute_population_nicopy(self):
        video = get_video_by_id('sm34734479')
        self.assertEqual(type(video.views), int, "'views' is expected to be an integer")
        self.assertEqual("sm34734479", video.id)
        self.assertEqual(251, video.duration)
        self.assertEqual(1551855600, video.timestamp)
