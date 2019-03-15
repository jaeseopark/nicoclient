from nico_client.daily_trending import DailyTrending
from nico_client.nicopy_adapter import get_video_info
from nico_client.playlist import Playlist
from nico_client.search_page import UtattemitaSearchPage
from nico_client.video import VIDEO_TYPE_UTATTEMITA, VIDEO_TYPE_VOCALOID_ORG, Video


class NicoClient(object):
    def get_daily_trending_videos(self):
        return DailyTrending().get_videos()

    def get_populated_copy(self, video):
        video_vars = vars(video)
        new_vars = get_video_info(video.id)
        for key in video_vars:
            video_vars[key] = new_vars.get(key) or video_vars[key]
        new_video = Video(**video_vars)
        new_video.details_populated = True
        return new_video

    def get_related_videos(self, video):
        if not video.details_populated:
            video = self.get_populated_copy(video)

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
