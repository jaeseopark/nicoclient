import json
from abc import ABC
from html.parser import HTMLParser

import requests


class HtmlPage(ABC):
    def __init__(self, html_string=None, url=None, headers={}, expected_codes=[200]):
        self.html_string = html_string
        self.status_code = None

        if url and html_string is None:
            response = requests.get(url=url, headers=headers)
            self.status_code = response.status_code
            if response.status_code in expected_codes:
                self.html_string = str(response.text)
            elif response.status_code == 403:
                raise PageAccessDeniedError(url)
            elif response.status_code == 404:
                raise PageNotFoundError(url)
            else:
                a_status = response.status_code
                e_status = json.dumps(expected_codes)
                text = str(response.text)
                raise RuntimeError(f"status_code={a_status} expected_codes={e_status} text='{text}'")


class PageError(Exception):
    pass


class PageAccessDeniedError(PageError):
    pass


class PageNotFoundError(PageError):
    pass


def to_json(content, raise_exception=False):
    def recursive_clean(node):
        if isinstance(node, list):
            for child in node:
                recursive_clean(child)
        elif isinstance(node, dict):
            if '__parent__' in node:
                del node['__parent__']
            for child in node.values():
                recursive_clean(child)

    class HTMLtoJSONParser(HTMLParser):
        def __init__(self, raise_exception=True):
            HTMLParser.__init__(self)
            self.doc = {}
            self.path = []
            self.cur = self.doc
            self.line = 0
            self.raise_exception = raise_exception

        @property
        def json(self):
            return self.doc

        def handle_starttag(self, tag, attrs):
            self.path.append(tag)
            attrs = {k: v for k, v in attrs}
            if tag in self.cur:
                if isinstance(self.cur[tag], list):
                    self.cur[tag].append({"__parent__": self.cur})
                    self.cur = self.cur[tag][-1]
                else:
                    self.cur[tag] = [self.cur[tag]]
                    self.cur[tag].append({"__parent__": self.cur})
                    self.cur = self.cur[tag][-1]
            else:
                self.cur[tag] = {"__parent__": self.cur}
                self.cur = self.cur[tag]

            for a, v in attrs.items():
                self.cur["#" + a] = v
            self.cur[""] = ""

        def handle_endtag(self, tag):
            if tag != self.path[-1] and self.raise_exception:
                raise Exception(
                    "html is malformed around line: {0} (it might be because of a tag <br>, <hr>, <img .. > not closed)".format(
                        self.line))
            del self.path[-1]
            memo = self.cur
            self.cur = self.cur["__parent__"]
            self.clean(memo)

        def handle_data(self, data):
            self.line += data.count("\n")
            if "" in self.cur:
                self.cur[""] += data

        def clean(self, values):
            keys = list(values.keys())
            for k in keys:
                v = values[k]
                if isinstance(v, str):
                    # print ("clean", k,[v])
                    c = v.strip(" \n\r\t")
                    if c != v:
                        if len(c) > 0:
                            values[k] = c
                        else:
                            del values[k]
            del values["__parent__"]

    parser = HTMLtoJSONParser(raise_exception=raise_exception)
    parser.feed(content)
    recursive_clean(parser.json)
    return parser.json
