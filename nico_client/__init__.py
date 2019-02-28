import re

import requests
import nicopy

name = "nico_client"


class NicoClient:
    def get_playlist(self, playlist_id):
        """
        :param playlist_id:
        :return: dictionary
        """
        return nicopy.get_mylist_info(mylist_id=playlist_id)

    def get_daily_trending_videos(self):
        url = "https://www.nicovideo.jp/ranking/fav/daily/sing"

        k_MYLIST_PATTERN = re.compile('(?<=<a href="/mylistcomment/video/)(.*?)">(.*?)(?=</a>)')

        r = requests.get(url)
        items = list(filter(lambda line: '<div class="itemData">' in line, str(r.text).split('\n')))

        video_ids = []
        for item in items:
            matches = k_MYLIST_PATTERN.search(item)
            video_id_pos = list(matches.regs[0])
            video_id_pos[1] = item.index('">', video_id_pos[0])
            video_ids.append(item[video_id_pos[0]:video_id_pos[1]])
        return video_ids
