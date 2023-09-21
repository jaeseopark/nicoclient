import dateutil.parser
import requests
from bs4 import BeautifulSoup

from nicoclient.model.video import Video


class Accessor(BeautifulSoup):
    def __init__(self, content):
        super().__init__(content, "html.parser")

    def __getitem__(self, key):
        return self.find(key).text


def to_duration(length: str) -> int:
    split = length.split(":")
    assert len(split) == 2
    min, sec = split
    return int(min) * 60 + int(sec)


def get_video_by_id(video_id) -> Video:
    url = f"https://ext.nicovideo.jp/api/getthumbinfo/{video_id}"
    r = requests.get(url)
    r.raise_for_status()

    accessor = Accessor(r.text)

    return Video(
        id=accessor["video_id"],
        title=accessor["title"],
        description=accessor["description"],
        views=int(accessor["view_counter"]),
        likes=int(accessor["mylist_counter"]),
        thumbnail_url=accessor["thumbnail_url"],
        duration=to_duration(accessor["length"]),
        timestamp=dateutil.parser.parse(accessor["first_retrieve"]).timestamp(),
        is_accessible=True,
    )
