import json
import logging

from nico_client.html_page.html_page import HtmlPage
from nico_client.model.video import Video

logger = logging.getLogger(__name__)


class Playlist(HtmlPage):
    def __init__(self, html_string=None, id=None):
        if html_string:
            HtmlPage.__init__(self, html_string=html_string)
        elif id:
            url = f"https://www.nicovideo.jp/mylist/{id}"
            HtmlPage.__init__(self, url=url)
        else:
            raise AssertionError('Need at least one parameter value')
        self.id = id
        self.__owner = None

    def get_videos(self):
        logger.info(f"Getting videos... playlist_id={self.id}")
        videos = []
        for line in [line.strip() for line in self.html_string.split('\n')]:
            if line.startswith('Mylist.preload'):
                idx_start = line.find('[')
                line = line[idx_start:-2]
                for item in json.loads(line):
                    item_data = item['item_data']
                    video = Video(
                        id=item_data['video_id'],
                        title=item_data['title'],
                        views=int(item_data['view_counter']),
                        likes=int(item_data['mylist_counter'])
                    )
                    video.thumbnail_url = item_data['thumbnail_url']
                    videos.append(video)

                return videos

        raise RuntimeError(f"keyword 'Mylist.preload' not found in HTML string playlist_id={self.id}")

    def get_owner_id(self):
        if not self.__owner:
            found = False
            logger.info(f"Retrieving owner info... playlist_id={self.id}")
            for line in self.html_string.split('\n'):
                if line.strip().startswith('mylist_owner: { user_id:'):
                    self.__owner = line.split(',')[0].split(':')[-1].strip()
                    found = True
            if not found:
                logger.warning(f'Owner not found playlist_id={self.id} status_code={self.status_code}')
        return self.__owner
