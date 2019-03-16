import json
import logging

import nicopy

from nico_client.html_page.html_page import PageError
from nico_client.html_page.video_page import VideoPage

logger = logging.getLogger(__name__)


def populate_details(video, method='nicopy'):
    """
    Populates the attributes in the given video object.
    :param video: Video object to be populated
    :param method: How the info will be retrieved. options = ['nicopy', 'html_parser']
    :return: None
    """
    if method == 'nicopy':
        info = get_info_via_nicopy(video.id)
    elif method == 'html_parser':
        info = VideoPage(id=video.id).get_video_info()
    else:
        raise AssertionError(f"invalid method='{method}'")
    __validate_info(info)
    video.setattrs(**info)


def __validate_info(json_object):
    """
    Ensure that the given json object has all the required keys. Throws AssertionError if a key (or keys) is missing.
    :param json_object: the JSON object to be evaluated
    :return: None
    """
    missing = []
    for key in ['tags', 'description', 'uploader_id', 'title', 'thumbnail_url', 'views', 'likes']:
        if key not in json_object:
            missing.append(key)
    if len(missing) > 0:
        raise AssertionError(f"missing keys={json.dumps(missing)}")


def get_info_via_nicopy(video_id):
    try:
        info_raw = nicopy.get_video_info(video_id)
        return {
            'tags': [tag['tag'] for tag in info_raw.get('tags')],
            'description': info_raw.get('description'),
            'uploader_id': info_raw.get('user_id'),
            'title': info_raw.get('title'),
            'thumbnail_url': info_raw.get('thumbnail_url'),
            'views': int(info_raw.get('view_counter')),
            'likes': int(info_raw.get('mylist_counter'))
        }
    except nicopy.ResponseFailError:
        raise PageError
