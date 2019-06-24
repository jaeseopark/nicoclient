import time

from bs4 import BeautifulSoup
from datetime import datetime

from nico_client.html_page.html_page import HtmlPage
from nico_client.model.video import Video
from nico_client.utils.time_utils import get_posix, get_posix_now

TIME_RANGE_VALUES = ['daily', 'weekly', 'monthly']
AGE_THRESHOLD_MAP = {
    'daily': 86400,
    'weekly': 86400 * 7,
    'monthly': 86400 * 30
}


class Trending(HtmlPage):
    def __init__(self, time_range=None, html_string=None, new_videos_only=True):
        if not time_range and not html_string:
            raise AssertionError('time_range or html_string must be provided')

        self.new_videos_only = new_videos_only
        self.time_range = None

        if html_string:
            HtmlPage.__init__(self, html_string=html_string)
            for tr in TIME_RANGE_VALUES:
                if self.html_string.count(f"/{tr}/") > 10:
                    self.time_range = tr
                    break
            if not self.time_range:
                raise RuntimeError('Cannot determine time range')
        else:
            if time_range not in TIME_RANGE_VALUES:
                raise AssertionError(f"invalid time_range='{time_range}'")
            self.time_range = time_range
            HtmlPage.__init__(self, url=f"https://www.nicovideo.jp/ranking/mylist/{time_range}/sing")

    def to_json(self):
        videos = []
        for item in self.html_string.split('<li class="item videoRanking'):
            if '<p class="itemTime' in item:
                root_node = BeautifulSoup('<li class="item videoRanking' + item, 'html.parser')

                time_str = root_node.find('div', {'class': 'videoList01Wrap'}).find('span').string
                time_obj = datetime.strptime(time_str, '%Y/%m/%d %H:%M')
                upload_time = (get_posix(time_obj) - 32400)  # 32400 is the difference between UTC & JST

                if self.new_videos_only:
                    age_threshold = AGE_THRESHOLD_MAP[self.time_range]
                    age = get_posix_now() - upload_time
                    if age > age_threshold:
                        # Do not append if the video is more than a day/week/month old
                        continue

                title_node = root_node.find('p', {'class': 'itemTitle ranking'}).find('a')

                videos.append({
                    'id': title_node['href'].strip('watch/'),
                    'title': title_node['title'],
                    'views': int(root_node.find('li', {'class': 'count view'}).find('span').string.replace(',', '')),
                    'likes': int(root_node.find('li', {'class': 'count mylist'}).find('span').string.replace(',', '')),
                    'upload_time': upload_time
                })

        return videos

    def get_videos(self):
        return self.to_json()


def get_trending_videos(time_range='daily', min_likes=0):
    vids = Trending(time_range=time_range).get_videos()
    return list(filter(lambda v: v['likes'] >= min_likes, vids))
