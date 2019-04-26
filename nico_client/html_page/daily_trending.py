import time

from bs4 import BeautifulSoup
from datetime import datetime

from nico_client.html_page.html_page import HtmlPage
from nico_client.model.video import Video
from nico_client.utils.time_utils import get_posix, get_posix_now


class DailyTrending(HtmlPage):
    def __init__(self, html_string=None):
        if html_string:
            HtmlPage.__init__(self, html_string=html_string)
        else:
            HtmlPage.__init__(self, url="https://www.nicovideo.jp/ranking/fav/daily/sing")

    def to_json(self):
        videos = []
        for item in self.html_string.split('<li class="item videoRanking'):
            if '<p class="itemTime' in item:
                root_node = BeautifulSoup('<li class="item videoRanking' + item, 'html.parser')

                time_str = root_node.find('div', {'class': 'videoList01Wrap'}).find('span').string
                time_obj = datetime.strptime(time_str, '%Y/%m/%d %H:%M')

                age = get_posix_now() - (get_posix(time_obj) - 32400)
                if age > 86400:
                    # Do not append if the video is more than a day old
                    continue

                title_node = root_node.find('p', {'class': 'itemTitle ranking'}).find('a')

                videos.append({
                    'id': title_node['href'].strip('watch/'),
                    'title': title_node['title'],
                    'views': int(root_node.find('li', {'class': 'count view'}).find('span').string.replace(',', '')),
                    'likes': int(root_node.find('li', {'class': 'count mylist'}).find('span').string.replace(',', '')),
                    'age': age
                })

        return videos

    def __get_videos(self):
        return [Video(**v) for v in self.to_json()]

    @staticmethod
    def get_videos():
        return DailyTrending().__get_videos()


def get_daily_trending_videos():
    return DailyTrending.get_videos()
