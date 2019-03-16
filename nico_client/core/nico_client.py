import logging

from nico_client.core import video_info_handler
from nico_client.core.video_finder import VideoFinder
from nico_client.html_page.daily_trending import DailyTrending
from nico_client.html_page.playlist import Playlist

logger = logging.getLogger(__name__)


def get_daily_trending_videos():
    return DailyTrending.get_videos()


def populate_details(video):
    video_info_handler.populate_details(video)


def get_related_videos(video, sort_by=None, limit=None):
    if not video.details_populated:
        populate_details(video)

    related_videos = VideoFinder.get_related_videos(video)

    if sort_by:
        related_videos.sort(key=lambda x: vars(x)[sort_by], reverse=True)

    if limit and limit < len(related_videos):
        related_videos = related_videos[:limit - 1]

    return related_videos


def get_videos_by_playlist_id(playlist_id):
    p = Playlist(id=playlist_id)
    return p.get_videos()
