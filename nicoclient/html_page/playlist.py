import json
import logging
from typing import List, Callable, Tuple

from bs4 import BeautifulSoup
from dateutil import parser as dateutil_parser

from nicoclient.html_page.html_page import HtmlPage
from nicoclient.model.playlist import Playlist
from nicoclient.model.video import Video

logger = logging.getLogger("nicoclient")


def preload(html_string: str) -> Tuple[str, str, List[Video]]:
    key_map = {
        'video_id': 'id',
        'view_counter': 'views',
        'mylist_counter': 'likes',
        'first_retrieve': 'timestamp',
        'last_res_body': 'description',
        'length_seconds': 'duration'
    }

    def get_videos():
        for line in [line.strip() for line in html_string.split('\n')]:
            if line.startswith('Mylist.preload'):
                idx_start = line.find('[')
                line = line[idx_start:-2]
                for item in json.loads(line):
                    item_data = item['item_data']
                    item_data["is_accessible"] = True
                    item_data['view_counter'] = int(item_data['view_counter'])
                    item_data['mylist_counter'] = int(item_data['mylist_counter'])
                    for key_old, key_new in key_map.items():
                        item_data[key_new] = item_data[key_old]
                    yield Video(**item_data)

    def get_owner():
        for line in html_string.split('\n'):
            if line.strip().startswith('mylist_owner: { user_id:'):
                return line.split(',')[0].split(':')[-1].strip()

    def get_name() -> str:
        return f"Playlist"  # TODO: use regex

    return get_owner(), get_name(), list(get_videos())


def initial_userpage(html_string: str) -> Tuple[str, str, List[Video]]:
    soup = BeautifulSoup(html_string, features="html.parser")
    element = soup.find(id="js-initial-userpage-data")
    json_string = element.get("data-initial-data")
    json_object = json.loads(json_string)
    nvapis = json_object['nvapi']

    def get_videos():
        for nvapi in nvapis:
            for item in nvapi['body']['data']['mylist']['items']:
                video = item['video']
                yield Video(
                    id=video["id"],
                    uploader_id=video["owner"]["id"],
                    title=video["title"],
                    views=video["count"]["view"],
                    likes=video["count"]["mylist"],
                    duration=video["duration"],
                    timestamp=dateutil_parser.parse(video["registeredAt"]).timestamp(),
                    thumbnail_url=video["thumbnail"]["url"],
                    is_accessible=True,  # assume accessible by default
                    description=video["shortDescription"]
                )

    def get_owner() -> str:
        for nvapi in nvapis:
            return nvapi["body"]["data"]["mylist"]["owner"]["id"]

    def get_name() -> str:
        for nvapi in nvapis:
            return nvapi["body"]["data"]["mylist"]["name"]

    return get_owner(), get_name(), list(get_videos())


class Parser:
    def __init__(self, execute):
        self.execute: Callable[[str], Tuple[str, str, List[Video]]] = execute


_PARSERS = [
    (lambda html_string: "Mylist.preload" in html_string, Parser(preload)),
    (lambda html_string: "js-initial-userpage-data" in html_string, Parser(initial_userpage)),
    # (lambda html_string: '<script type="application/ld+json">' in html_string, Parser(application_ld_json))
]


def get_html_parser(html_string: str) -> Parser:
    for predicate, parser in _PARSERS:
        if predicate(html_string):
            logger.info(f"parser found; parser_name={parser.execute.__name__}")
            return parser

    raise RuntimeError("Cannot find any parsers for the given html string")


class PlaylistPage(HtmlPage):
    playlist: Playlist

    def __init__(self, id: str):
        HtmlPage.__init__(self, url=f"https://www.nicovideo.jp/mylist/{id}")
        self.id = id
        self._parse()

    def _parse(self):
        parser = get_html_parser(self.html_string)
        owner_id, name, videos = parser.execute(self.html_string)
        self.playlist = Playlist(
            id=self.id,
            name=name,
            owner_id=owner_id,
            videos=videos,
            is_monitored=False
        )


def get_playlist(playlist_id: str) -> Playlist:
    return PlaylistPage(id=playlist_id).playlist
