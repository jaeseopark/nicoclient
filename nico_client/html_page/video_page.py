from nico_client.html_page import HtmlPage

url_regex_str = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'


class VideoPage(HtmlPage):
    @property
    def raw_description(self):
        return self.to_json()['raw_description']

    def to_json(self):
        desc = self.html_string
        # TODO do stuff

        return {
            'raw_description': self.raw_description
        }
