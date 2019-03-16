import logging

from nicopy import ResponseFailError

from nico_client.core import nicopy_adapter
from nico_client.html_page.video_page import VideoPage

logger = logging.getLogger(__name__)


def populate_details(video):
    """
    Populates the attributes in the given video object.
    :param video: Video object to be populated
    :return: None
    """
    try:
        info = nicopy_adapter.get_video_info(video.id)
    except ResponseFailError:
        logger.warning(f"video='{id}' raised a ResponseFailError; falling back to HTML parser...")
        info = VideoPage(video.id).get_video_info()

    video.setattrs(**info)
