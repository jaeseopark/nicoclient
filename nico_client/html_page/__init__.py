from abc import abstractmethod

import requests


class HtmlPage(object):
    def __init__(self, html_string=None, url=None, headers={}, expected_codes=[200]):
        self.html_string = html_string

        if url and html_string is None:
            response = requests.get(url=url, headers=headers)
            if response.status_code not in expected_codes:
                self.html_string = str(response.text)
            else:
                raise RuntimeError(f"status_code={response.status_code} text='{str(response.text)}'")

        self.html_string = self.html_string.replace('<!DOCTYPE html>', '')

    @abstractmethod
    def to_json(self):
        pass
