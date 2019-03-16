from nicopy import nicopy, ResponseFailError
import logging

logger = logging.getLogger(__name__)


def get_video_info(id):
    try:
        video_info = nicopy.get_video_info(video_id=id)
        mapped_video_info = {
            'tags': [tag['tag'] for tag in video_info.get('tags')],
            'description': video_info.get('description'),
            'uploader_id': video_info.get('user_id'),
            'title': video_info.get('title'),
            'thumbnail_url': video_info.get('thumbnail_url'),
            'views': int(video_info.get('view_counter')),
            'likes': int(video_info.get('mylist_counter'))
        }
    except ResponseFailError:
        logger.warning(f"ResponseFailError video='{id}'; returning empty values")
        mapped_video_info = {
            'tags': [],
            'description': '',
            'uploader_id': '',
            'title': '',
            'thumbnail_url': '',
            'views': 0,
            'likes': 0
        }
    return mapped_video_info


def populate_details(video):
    """
    Populates the attributes in the given video object.
    Ideally, this function should reside in nico_client, but other files in the module use this function and there is
    a risk of having cyclic dependency.
    :param video: Video object to be populated
    :return: None
    """
    video.setattrs(**get_video_info(video.id))
