import json
import logging

from nicopy import ResponseFailError, nicopy

from nico_client.html_page.video_page import VideoPage

logger = logging.getLogger(__name__)


def populate_details(video):
    """
    Populates the attributes in the given video object.
    :param video: Video object to be populated
    :return: None
    """
    info = get_info_via_nicopy(video.id)
    if info is None:
        logger.warning(f"video='{id}' raised a ResponseFailError; falling back to HTML parser...")
        info = VideoPage(id=video.id).get_video_info()

    __validate_info(info)
    video.setattrs(**info)


def __validate_info(json_object):
    missing = []
    for key in ['tags', 'description', 'uploader_id', 'title', 'thumbnail_url', 'views', 'likes']:
        if key not in json_object:
            missing.append(key)
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
    except ResponseFailError:
        return None
