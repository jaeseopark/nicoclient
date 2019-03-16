import logging
from abc import ABC, abstractmethod

from nico_client.core.video_info_handler import populate_details
from nico_client.html_page.html_page import PageError
from nico_client.html_page.playlist import Playlist
from nico_client.html_page.search_page import UtattemitaSearchPage
from nico_client.model.video import VIDEO_TYPE_UTATTEMITA, VIDEO_TYPE_VOCALOID_ORG, Video

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
            return VideoFinderDummy(video)

    @abstractmethod
    def get_related_videos_impl(self):
        pass


class VideoFinderDummy(VideoFinder):
    def get_related_videos_impl(self):
        return []


class VideoFinderUtattemita(VideoFinder):
    def get_related_videos_impl(self):
        related_videos = []
        for ref in self.video.find_references():
            logger.info(f"Evaluating ref={ref}")
            if ref.startswith('sm'):
                referenced_video = Video(id=ref)
                try:
                    populate_details(referenced_video)
                    if referenced_video.video_type == VIDEO_TYPE_VOCALOID_ORG:
                        related_videos.append(referenced_video)
                    else:
                        logger.info(f"{referenced_video.id} is not a vocaloid original video; skipping")
                except PageError:
                    logger.info(f"PageError with video_id='{referenced_video.id}'; skipping")
            elif ref.startswith('mylist/'):
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
        search_results = UtattemitaSearchPage(self.video)
        related_videos += search_results.get_videos()
        return related_videos


def get_related_videos(video, sort_by=None, limit=None):
    if not video.details_populated:
        try:
            populate_details(video)
        except PageError as e:
            logger.warning(f"PagerError with video_id={video.id} error='{str(e)}'; returning an empty array")
            return []

    related_videos = VideoFinder.get_related_videos(video)

    if sort_by:
        related_videos.sort(key=lambda x: vars(x)[sort_by], reverse=True)

    if limit and limit < len(related_videos):
        related_videos = related_videos[:limit - 1]

    return related_videos
