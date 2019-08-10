import logging
from abc import ABC, abstractmethod

from nicoclient.core.video_info_handler import get_metadata
from nicoclient.html_page.html_page import PageError
from nicoclient.html_page.playlist import Playlist
from nicoclient.html_page.search_page import UtattemitaSearchPage
from nicoclient.model.video import VIDEO_TYPE_VOCALOID_ORG, Video

logger = logging.getLogger(__name__)


class VideoFinder(ABC):
    def __init__(self, video):
        self.video = video

    @staticmethod
    def get_related_videos(video: Video):
        finder = VideoFinder.__get_finder_instance(video)
        return finder.get_related_videos_impl()

    @staticmethod
    def __get_finder_instance(video):
        if video.video_type == VIDEO_TYPE_VOCALOID_ORG:
            return VideoFinderVocaloidOriginal(video)
        else:
            return VideoFinderUtattemita(video)

    @abstractmethod
    def get_related_videos_impl(self):
        pass


class VideoFinderUtattemita(VideoFinder):
    def get_related_videos_impl(self):
        related_videos = []
        for ref in self.video.find_references():
            logger.info(f"Evaluating ref={ref}")
            if ref.startswith('mylist/'):
                playlist_id = ref.split('/')[-1]
                try:
                    p = Playlist(id=playlist_id)
                    logger.info(f"playlist='{ref}' owner='{p.get_owner_id()}'")
                    if p.get_owner_id() == self.video.uploader_id:
                        related_videos += p.get_videos()
                    else:
                        logger.info('owner does not match; skipping')
                except PageError:
                    logger.warning(f"ref='{ref}' not accessible; skipping")
        return related_videos


class VideoFinderVocaloidOriginal(VideoFinder):
    def get_related_videos_impl(self):
        related_videos = []
        search_results = UtattemitaSearchPage(video=self.video)
        related_videos += search_results.get_videos()
        return related_videos


def get_related_videos(video_id:str):
    metadata = get_metadata(video_id)
    video = Video(id=video_id)
    video.setattrs(**metadata)

    return VideoFinder.get_related_videos(video)
