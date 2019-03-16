from nico_client.html_page.html_page import HtmlPage


class VideoPage(HtmlPage):
    def __init__(self, html_string, id):
        if html_string:
            HtmlPage.__init__(self, html_string=html_string)
        elif id:
            url = f"https://www.nicovideo.jp/watch/{id}"
            HtmlPage.__init__(self, url=url)
        else:
            raise AssertionError('Need at least one parameter value')
        self.id = id

    def get_video_info(self):
        raise NotImplementedError('not implemented yet')