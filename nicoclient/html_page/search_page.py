from nicoclient.html_page.html_page import HtmlPage, to_json
from nicoclient.model.video import Video


class UtattemitaSearchPage(HtmlPage):
    def __init__(self, html_string=None, video=None):
        if html_string:
            HtmlPage.__init__(self, html_string=html_string)
        elif video:
            url = f'https://www.nicovideo.jp/search/{video.id}%20%E6%AD%8C%E3%81%A3%E3%81%A6%E3%81%BF%E3%81%9F?page=1&sort=m&order=d'
            HtmlPage.__init__(self, url=url)
        else:
            raise AssertionError('Need at least one parameter value')

    def __get_videos_as_json(self):
        start_keyword = '<li class="item" data-video-item data-video-id="'
        end_keyword = '</li>'

        videos = []
        recording_mode = False
        video_string_array = []

        for line in self.html_string.split('\n'):
            if line.strip().startswith(start_keyword):
                recording_mode = True

            if not recording_mode:
                continue

            video_string_array.append(line)

            if line.strip() == end_keyword:
                recording_mode = False
                json_object = to_json('\n'.join(video_string_array))
                videos.append(json_object)
                video_string_array = []

        return videos

    def __to_video(self, video_json):
        video = Video()
        video.id = video_json['li']['#data-video-id']

        for outer_div in video_json['li']['div']['div']:
            outer_div_class = outer_div['#class']
            if outer_div_class == 'uadWrap':
                for inner_div in outer_div['div']['div']:
                    inner_div_class = inner_div['#class']
                    if inner_div_class == 'itemThumb':
                        video.thumbnail_url = inner_div['a']['img']['#data-original']
            elif outer_div_class == 'itemContent':
                video.title = outer_div['p']['a']['#title']
                for inner_div in outer_div['div']:
                    inner_div_class = inner_div['#class']
                    if inner_div_class == 'itemData':
                        for item_data_element in inner_div['ul']['li']:
                            ide_class = item_data_element['#class']
                            if ide_class == 'count view':
                                video.views = int(item_data_element['span'][''].replace(',', ''))
                            elif ide_class == 'count mylist':
                                video.likes = int(item_data_element['span']['a'][''].replace(',', ''))
        return video

    def get_videos(self):
        return [vars(self.__to_video(j)) for j in self.__get_videos_as_json()]
