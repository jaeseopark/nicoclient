import unittest

from nicoclient import get_metadata


class TestVideoInfoHandler(unittest.TestCase):
    def test_video_attribute_population_nicopy(self):
        metadata = get_metadata('sm34734479')
        self.assertEqual(type(metadata['views']), int, "'views' is expected to be an integer")
