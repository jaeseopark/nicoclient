import json
import logging

from nicoclient.html_page.video_page import VideoPage

logger = logging.getLogger(__name__)


def get_metadata(video_id: str, method='html_parser'):
    """
    Populates the attributes in the given video object.
    :param video: dictionary to be populated
    :param method: How the info will be retrieved. options = ['html_parser']
    :return: None
    """
    if method == 'html_parser':
        metadata = VideoPage(id=video_id).get_video_metadata()
    else:
        raise AssertionError(f"invalid method='{method}'")
    __validate_fields(metadata)
    return metadata


def __validate_fields(json_object):
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
