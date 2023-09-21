import datetime
import logging
from typing import List, Iterator

import dateutil.parser
import requests

from nicoclient.model.video import Video

_SEARCH_LIMIT = 25

logger = logging.getLogger("nicoclient")
from datetime import datetime, timedelta


class NicoSearchApiV2Client:
    """
    https://site.nicovideo.jp/search-api-docs/snapshot
    """

    @staticmethod
    def search(query: str, param_override: dict = None) -> Iterator[Video]:
        url = "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
        headers = {"User-Agent": "nicoclient"}
        params = dict(
            q=query,
            targets="title,description,tags",
            fields="contentId,title,description,userId,mylistCounter,viewCounter,lengthSeconds,thumbnailUrl,startTime",
            _sort="-viewCounter",
            _limit=_SEARCH_LIMIT,
            _context="nicoclient"
        )
        if param_override:
            params.update(param_override)

        response = requests.request("GET", url, headers=headers, params=params)
        response.raise_for_status()

        for item in response.json()["data"]:
            yield Video(
                id=item["contentId"],
                likes=item["mylistCounter"],
                duration=item["lengthSeconds"],
                views=item["viewCounter"],
                thumbnail_url=item["thumbnailUrl"],
                description=item["description"],
                timestamp=dateutil.parser.parse(item["startTime"]).timestamp(),
                uploader_id=item["userId"],
                title=item["title"],
                is_accessible=True
            )

    @staticmethod
    def search_daily_trending(min_likes=0):
        yesterday = datetime.now() - timedelta(1)
        return list(NicoSearchApiV2Client.search(
            query="歌ってみた",
            param_override={
                "targets": "tagsExact",
                "filters[startTime][gte]": yesterday.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "filters[mylistCounter][gte]": min_likes
            }
        ))


def search_utattemita_videos(video_id: str) -> List[Video]:
    return list(NicoSearchApiV2Client.search(f"{video_id} 歌ってみた"))


search_daily_trending_utatttemita_videos = NicoSearchApiV2Client.search_daily_trending
