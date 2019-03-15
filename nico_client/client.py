from nico_client.daily_trending import DailyTrending
from nico_client.nicopy_adapter import get_video_info
from nico_client.playlist import Playlist
from nico_client.search_page import UtattemitaSearchPage
from nico_client.video import VIDEO_TYPE_UTATTEMITA, VIDEO_TYPE_VOCALOID_ORG, Video


class NicoClient(object):
    def get_daily_trending_videos(self):
        return DailyTrending().get_videos()

    def populate_details(self, video):
        video.setattrs(**get_video_info(video.id))

    def get_related_videos(self, video):
        if not video.details_populated:
            self.populate_details(video)

        if video.video_type == VIDEO_TYPE_UTATTEMITA:
            related_videos = []
            for ref in video.find_references():
                if ref.startswith('sm'):
                    referenced_video = Video(id=ref)
                    self.populate_details(referenced_video)
                    related_videos.append(referenced_video)
                elif ref.startswith('mylist/'):
                    p = Playlist(id=ref.split('/')[-1])
                    related_videos += p.get_videos()
            return related_videos

        elif video.video_type == VIDEO_TYPE_VOCALOID_ORG:
            search_results = UtattemitaSearchPage(video)
            return search_results.get_videos()
        else:
            return []

    def get_videos_by_playlist_id(self, playlist_id):
        p = Playlist(id=playlist_id)
        return p.get_videos()
