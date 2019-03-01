import requests
from nicopy import get_mylist_info

from nico_client.html_page.daily_trending import DailyTrending
from nico_client.playlist import Playlist


class NicoClient(object):
    def get_playlist(self, playlist_id):
        playlist_dict = get_mylist_info(mylist_id=playlist_id)
        return Playlist(playlist_dict)

    def get_daily_trending_videos(self):
        url = "https://www.nicovideo.jp/ranking/fav/daily/sing"
        r = requests.get(url)
        trending = DailyTrending(str(r.text))
        return trending.get_videos()
