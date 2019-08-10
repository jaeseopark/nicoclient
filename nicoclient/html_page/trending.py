import logging
from datetime import datetime

from bs4 import BeautifulSoup, Tag

from nicoclient.html_page.html_page import HtmlPage
from nicoclient.utils.time_utils import get_posix, get_posix_now

logger = logging.getLogger(__name__)

VIDEO_CLASSES = ["MediaObject", "RankingMainVideo"]


class Trending(HtmlPage):
    def __init__(self, html_string=None, new_videos_only=True):
        self.new_videos_only = new_videos_only

        if html_string:
            HtmlPage.__init__(self, html_string=html_string)
        else:
            url = "https://www.nicovideo.jp/ranking/genre/music_sound?term=24h&tag=%E6%AD%8C%E3%81%A3%E3%81%A6%E3%81%BF%E3%81%9F"
            HtmlPage.__init__(self, url=url)

    def __node_to_video(self, node: Tag):
        thumbnail_node = node.find('div', {'class': 'Thumbnail-image'})
        title_node = node.find('a', {'class': 'RankingMainVideo-title'})
        desc_node = node.find('div', {'class': 'RankingMainVideo-description'})
        views_node = node.find('span', {'class': 'VideoMetaCount-view'})
        likes_node = node.find('span', {'class': 'VideoMetaCount-mylist'})
        upload_time_node = node.find('span', {'class': 'RankingMainVideo-uploaded'})
        upload_time_str = upload_time_node.text.replace('\n', '').strip()[:16]

        # upload_time is being subtracted by 32400, because 32400 is the difference between UTC & JST

        return {
            'id': node.attrs.get('data-video-id'),
            'title': title_node.text,
            'views': int(views_node.text.replace(',', '')),
            'likes': int(likes_node.text.replace(',', '')),
            'upload_time_str': upload_time_str,
            'upload_time': get_posix(datetime.strptime(upload_time_str, '%Y/%m/%d %H:%M')) - 32400,
            'thumbnail_url': thumbnail_node.attrs.get('data-background-image'),
            'description': desc_node.text
        }

    def to_json(self):
        videos = []
        html_node = BeautifulSoup(self.html_string, 'html.parser')
        container_node = html_node.find('div', {'class': 'RankingVideoListContainer'})
        for child in container_node.children:
            if isinstance(child, Tag):
                cls_list = child.attrs.get('class', [])
                if all(map(lambda vid_cls: vid_cls in cls_list, VIDEO_CLASSES)):
                    video = self.__node_to_video(child)
                    if self.new_videos_only:
                        current_time = get_posix_now()
                        age = current_time - video['upload_time']

                        if age > 86400:
                            # Do not append if the video is more than a day old
                            continue

                    videos.append(video)

        return videos

    def get_videos(self):
        return self.to_json()


def get_trending_videos(min_likes=0):
    vids = Trending().get_videos()
    return list(filter(lambda v: v['likes'] >= min_likes, vids))
