from abc import abstractmethod


class HtmlPage(object):
    def __init__(self, html_string):
        self.html_string = html_string

    @abstractmethod
    def to_json(self):
        pass