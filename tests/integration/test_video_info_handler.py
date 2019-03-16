from nico_client import populate_details
from nico_client.model.video import Video
from tests import IntegrationTest


class TestVideoInfoHandler(IntegrationTest):
    def test_video_attribute_population(self):
        video = Video(id='sm34734479')
        self.assertIsNone(video.views)
        populate_details(video)
        self.assertEqual(type(video.views), int, "video.views is expected to be an integer")
