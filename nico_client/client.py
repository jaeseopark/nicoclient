from nicopy import get_mylist_info, nicopy

from nico_client.html_page.daily_trending import DailyTrending
from nico_client.html_page.search_page import UtattemitaSearchPage
from nico_client.playlist import Playlist
from nico_client.video import VIDEO_TYPE_UTATTEMITA, VIDEO_TYPE_VOCALOID_ORG


class NicoClient(object):
    def get_playlist(self, playlist_id):
        playlist_dict = get_mylist_info(mylist_id=playlist_id)
        return Playlist(playlist_dict)

    def get_daily_trending_videos(self):
        trending = DailyTrending()
        return trending.get_videos()

    def populate_details(self, video):
        # TODO: raw_description
        video_info = nicopy.get_video_info(video.id)

        video.tags = [tag['tag'] for tag in video_info.get('tags')]
        video.description = video_info.get('description')
        video.uploader_id = video_info.get('user_id')
        video.title = video_info.get('title')
        video.thumbnail_url = video_info.get('thumbnail_url')
        video.views = video_info.get('view_counter')
        video.likes = video_info.get('mylist_counter')
        video.details_populated = True

    def get_related_videos(self, video):
        if not video.details_populated:
            self.populate_details(video)

        if video.video_type == VIDEO_TYPE_UTATTEMITA:
            # TODO: return other videos in the playlist
            return []
        elif video.video_type == VIDEO_TYPE_VOCALOID_ORG:
            search_results = UtattemitaSearchPage(video)
            return search_results.get_videos()
        else:
            return []
