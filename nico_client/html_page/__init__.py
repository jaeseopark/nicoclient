from abc import abstractmethod

import requests


class HtmlPage(object):
    def __init__(self, html_string=None, url=None, headers={}, expected_codes=[200]):
        self.html_string = html_string

        if url and html_string is None:
            response = requests.get(url=url, headers=headers)
            if response.status_code in expected_codes:
                self.html_string = str(response.text)
            else:
                msg = f"status_code={response.status_code} expected_codes={expected_codes} text='{str(response.text)}'"
                raise RuntimeError(msg)

    @abstractmethod
    def to_json(self):
        pass
