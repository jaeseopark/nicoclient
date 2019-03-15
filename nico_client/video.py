import json
import re

VIDEO_TYPE_UTATTEMITA = 'utattemita'
VIDEO_TYPE_VOCALOID_ORG = 'org'
VIDEO_TYPE_INSUFFICIENT_DATA = 'insufficient_data'
VIDEO_TYPE_UNCATEGORIZED = 'uncategorized'


class Video(object):
    def __init__(self, id=None, title=None, url=None, views=None, likes=None, *args, **kwargs):
        self.id = id
        self.views = views
        self.likes = likes
        self.thumbnail_url = None
        self.title = title
        self.tags = None
        self.description = None
        self.uploader_id = None
        self.details_populated = False

        if url and self.id is None:
            self.id = url.split('/')[-1].split('?')[0]

    def __str__(self):
        return json.dumps(vars(self))

    @property
    def video_type(self):
        if not self.tags:
            return VIDEO_TYPE_INSUFFICIENT_DATA
        if '歌ってみた' in self.tags or 'Sang_it' in self.tags:
            return VIDEO_TYPE_UTATTEMITA
        elif 'Vocaloid' in self.html.tags:
            return VIDEO_TYPE_VOCALOID_ORG
        else:
            return VIDEO_TYPE_UNCATEGORIZED

    def find_references(self):
        if self.description is None:
            raise AssertionError('description is required')

        refs = []
        for keyword in ['sm', 'mylist/']:
            index_set = [m.start() for m in re.finditer(keyword, self.description)]
            for i_start in index_set:
                i_end = None
                for j in range(i_start + len(keyword), len(self.description)):
                    if not self.description[j].isdigit():
                        i_end = j
                        break
                refs.append(self.description[i_start:i_end])

        return refs
