from nico_client.core import video_finder
from nico_client.model.video import Video
from tests.integration import IntegrationTest


class TestVideoFinder(IntegrationTest):
    def test_related_videos(self):
        for video_id in ['sm34775615', 'sm34734479']:
            with self.subTest(video_id=video_id):
                video = Video(id=video_id)
                videos = video_finder.get_related_videos(video)
                self.assertTrue(len(videos) > 1)
