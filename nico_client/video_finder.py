import logging
from abc import ABC, abstractmethod

from nico_client.html_page import PageError
from nico_client.playlist import Playlist
from nico_client.search_page import UtattemitaSearchPage
from nico_client.video import VIDEO_TYPE_UTATTEMITA, VIDEO_TYPE_VOCALOID_ORG, Video

logger = logging.getLogger(__name__)


class VideoFinder(ABC):
    def __init__(self, video):
        self.video = video

    @staticmethod
    def get_related_videos(video):
        finder = VideoFinder.__get_finder_instance(video)
        return finder.get_related_videos_impl()

    @staticmethod
    def __get_finder_instance(video):
        if video.video_type == VIDEO_TYPE_UTATTEMITA:
            return VideoFinderUtattemita(video)
        elif video.video_type == VIDEO_TYPE_VOCALOID_ORG:
            return VideoFinderVocaloidOriginal(video)
        else:
            logger.info(f"video_type={video.video_type} has no corresponding VideoFinder; skipping")
            return []

    @abstractmethod
    def get_related_videos_impl(self):
        pass


class VideoFinderUtattemita(VideoFinder):
    def get_related_videos_impl(self):
        related_videos = []
        for ref in self.video.find_references():
            if ref.startswith('sm'):
                referenced_video = Video(id=ref)
                self.populate_details(referenced_video)
                related_videos.append(referenced_video)
            elif ref.startswith('mylist/'):
                playlist_id = ref.split('/')[-1]
                try:
                    p = Playlist(id=playlist_id)
                    if p.get_owner_id() == self.video.uploader_id:
                        related_videos += p.get_videos()
                    else:
                        logger.info(f"playlist='{ref}' owner='{p.get_owner_id()}'")
                except PageError:
                    logger.warning(f"ref='{ref}' not accessible; skipping")
        return related_videos


class VideoFinderVocaloidOriginal(VideoFinder):
    def get_related_videos_impl(self):
        related_videos = []
        search_results = UtattemitaSearchPage(self.video)
        related_videos += search_results.get_videos()
        return related_videos
