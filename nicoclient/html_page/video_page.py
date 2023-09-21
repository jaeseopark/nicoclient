import json
import logging
from typing import Callable

from bs4 import BeautifulSoup
from dateutil import parser as dateutil_parser

from nicoclient.html_page.html_page import HtmlPage
from nicoclient.model.video import Video
from nicoclient.utils.time_utils import str_to_posix

logger = logging.getLogger("nicoclient")


def parse_json(html_string: str) -> Video:
    soup = BeautifulSoup(html_string, features="html.parser")
    div = soup.find(id="js-initial-watch-data")
    json_str = div.get("data-api-data")
    json_object = json.loads(json_str)
    video = json_object['video']

    return Video(
        id=video["id"],
        description=video['description'],
        uploader_id=json_object['owner']['id'],
        title=video['title'],
        thumbnail_url=video['thumbnail']['url'],
        views=int(video['count']['view']),
        likes=int(video['count']['mylist']),
        timestamp=dateutil_parser.parse(video["registeredAt"]).timestamp(),
        duration=video['duration'],
        is_accessible=True
    )


def parse_non_json(html_string: str) -> Video:
    root_node = BeautifulSoup(html_string, 'html.parser')
    id_node = root_node.find('meta', {"property": "og:url"})
    title_node = root_node.find('h1', {'class': 'VideoTitle'})
    user_node = root_node.find('div', {'class': 'VideoOwnerIcon'})
    user_id = user_node.find('a')['href'].split('/')[-1]
    thumbnail_node = root_node.find('meta', {'itemprop': "thumbnailUrl"})
    view_count_node = root_node.find('span', {'class': "VideoViewCountMeta-counter"})
    like_count_node = root_node.find('span', {'class': "MylistCountMeta-counter"})
    description_node = root_node.find('p', {'class': 'VideoDescription-text'})
    time_node = root_node.find('time', {'class': 'VideoUploadDateMeta-dateTimeLabel'})
    return Video(
        id=id_node['content'].split("/")[-1],
        description=description_node.get_text(),
        uploader_id=user_id,
        title=title_node.get_text(),
        thumbnail_url=thumbnail_node['content'],
        views=int(view_count_node.find('span').get_text().replace(',', '')),
        likes=int(like_count_node.find('span').get_text().replace(',', '')),
        timestamp=str_to_posix(time_node.get_text()) - 32400,
        duration=0,
        is_accessible=True
    )


class Parser:
    def __init__(self, execute: Callable[[str], Video]):
        self.execute = execute


_PARSERS = [
    (lambda html_string: 'js-initial-watch-data' in html_string, Parser(parse_json)),
    (lambda html_string: '<h1 class="VideoTitle">' in html_string, Parser(parse_non_json))
]


def _get_html_parser(html_string: str) -> Parser:
    for predicate, parser in _PARSERS:
        if predicate(html_string):
            logger.info(f"parser found; parser_name={parser.execute.__name__}")
            return parser

    raise RuntimeError("Cannot find any parsers for the given html string")


class VideoPage(HtmlPage):
    video: Video

    def __init__(self, html_string=None, id=None):
        HtmlPage.__init__(self, html_string=html_string, url=f"https://www.nicovideo.jp/watch/{id}")
        self._parse()

    def _parse(self):
        parser = _get_html_parser(self.html_string)
        self.video = parser.execute(self.html_string)


def get_video_by_id(video_id: str) -> Video:
    return VideoPage(id=video_id).video
