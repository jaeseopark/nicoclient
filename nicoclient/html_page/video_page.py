import json
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from nicoclient.html_page.html_page import HtmlPage
from nicoclient.utils.time_utils import str_to_posix


class VideoPage(HtmlPage):
    def __init__(self, html_string=None, id=None):
        if html_string:
            HtmlPage.__init__(self, html_string=html_string)
        elif id:
            url = f"https://www.nicovideo.jp/watch/{id}"
            HtmlPage.__init__(self, url=url)
        else:
            raise AssertionError('Need at least one parameter value')
        self.id = id

    def get_video_metadata(self):
        inner_parser = VideoPageInnerParser.get_inner_parser(self.html_string)
        return inner_parser.get_video_info()


class VideoPageInnerParser(ABC):
    def __init__(self, html_string):
        self.html_string = html_string

    @staticmethod
    def get_inner_parser(html_string):
        if 'js-initial-watch-data' in html_string:
            cls = VideoPageInnerParserWithJson
        elif '<h1 class="VideoTitle">' in html_string:
            cls = VideoPageInnerParserWithoutJson
        else:
            raise NotImplementedError
        return cls(html_string)

    @abstractmethod
    def get_video_info(self):
        pass


class VideoPageInnerParserWithJson(VideoPageInnerParser):
    def get_video_info(self):
        for line in [x.strip() for x in self.html_string.split('\n')]:
            if 'js-initial-watch-data' in line:
                json_object = self.line_to_json(line)
                return self.map_video_attributes(json_object)
        raise NotImplementedError('handle edge cases here')

    def map_video_attributes(self, json_object):

        return {
            'tags': [tag['name'] for tag in json_object['tags']],
            'description': json_object['video']['originalDescription'],
            'uploader_id': json_object['owner']['id'],
            'title': json_object['video']['title'],
            'thumbnail_url': json_object['video']['thumbnailURL'],
            'views': int(json_object['video']['viewCount']),
            'likes': int(json_object['video']['mylistCount']),
            'upload_time': str_to_posix(json_object['video']['postedDateTime']) - 32400
        }

    def line_to_json(self, line):
        root_node = BeautifulSoup(line, 'html.parser')
        div_node = root_node.find('div', {'id': 'js-initial-watch-data'})
        json_string = div_node['data-api-data']
        return json.loads(json_string)


class VideoPageInnerParserWithoutJson(VideoPageInnerParser):
    def get_video_info(self):
        root_node = BeautifulSoup(self.html_string, 'html.parser')
        title_node = root_node.find('h1', {'class': 'VideoTitle'})
        user_node = root_node.find('div', {'class': 'VideoOwnerIcon'})
        user_id = user_node.find('a')['href'].split('/')[-1]
        tags = self.to_tag_array(root_node.find('ul', {'class': 'TagList'}))
        thumbnail_node = root_node.find('meta', {'itemprop': "thumbnailUrl"})
        view_count_node = root_node.find('span', {'class': "VideoViewCountMeta-counter"})
        like_count_node = root_node.find('span', {'class': "MylistCountMeta-counter"})
        description_node = root_node.find('p', {'class': 'VideoDescription-text'})
        time_node = root_node.find('time', {'class': 'VideoUploadDateMeta-dateTimeLabel'})
        return {
            'tags': tags,
            'description': description_node.get_text(),
            'uploader_id': user_id,
            'title': title_node.get_text(),
            'thumbnail_url': thumbnail_node['content'],
            'views': int(view_count_node.find('span').get_text().replace(',', '')),
            'likes': int(like_count_node.find('span').get_text().replace(',', '')),
            'upload_time': str_to_posix(time_node.get_text()) - 32400
        }

    def to_tag_array(self, tag_node):
        f = filter(lambda aa: True, tag_node.find_all('a', {'class': 'Link TagItem-name', 'rel': 'tag'}))
        return [a.get_text() for a in f]
