import unittest

from nicoclient.core import video_finder


class TestVideoFinder(unittest.TestCase):
    def test_related_videos_vocaloid_org(self):
        videos = video_finder.get_related_videos('sm32076378')
        self.assertTrue(len(videos) > 1)
