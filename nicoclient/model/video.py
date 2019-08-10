import json
import logging
import re

VIDEO_TYPE_UTATTEMITA = 'utattemita'
VIDEO_TYPE_VOCALOID_ORG = 'vocaloid_org'
VIDEO_TYPE_NOT_INITIALIZED = 'not_initialized'
VIDEO_TYPE_UNKNOWN = 'unknown'

logger = logging.getLogger(__name__)


class Video(object):
    def __init__(self, id=None, title=None, url=None, views=None, likes=None, upload_time=None, *args, **kwargs):
        self.id = id
        self.views = views
        self.likes = likes
        self.thumbnail_url = None
        self.title = title
        self.upload_time = upload_time or -1
        self.tags = None
        self.description = None
        self.uploader_id = None
        self.details_populated = False
        self.video_type = VIDEO_TYPE_NOT_INITIALIZED

        if url and self.id is None:
            self.id = url.split('/')[-1].split('?')[0]

    def __str__(self):
        attrs = vars(self)
        attrs['title'] = self.title
        attrs['description'] = self.description
        attrs['tags'] = self.tags

        return json.dumps(attrs)

    def find_references(self):
        if self.description is None:
            raise AssertionError('description is required')

        refs = list()
        for keyword in ['sm', 'mylist/']:
            index_set = [m.start() for m in re.finditer(keyword, self.description)]
            for i_start in index_set:
                i_end = None
                for j in range(i_start + len(keyword), len(self.description)):
                    if not self.description[j].isdigit():
                        i_end = j
                        break
                ref = self.description[i_start:i_end]
                if len(ref) > len(keyword):
                    if ref not in refs:
                        refs.append(ref)
                    logger.info(f"ref={ref} has been added to the list")
                else:
                    logger.info(f"ref={ref} is not valid; skipping")

        return refs

    def __init_tags(self):
        self.tags = self.tags or []
        if '歌ってみた' in self.tags or 'Sang_it' in self.tags:
            self.video_type = VIDEO_TYPE_UTATTEMITA
        elif 'Vocaloid' in self.tags or 'VOCALOID' in self.tags:
            self.video_type = VIDEO_TYPE_VOCALOID_ORG
        else:
            self.video_type = VIDEO_TYPE_UNKNOWN

    def setattrs(self, **kwargs):
        original_vars = vars(self)
        for k, v in kwargs.items():
            if k in original_vars:
                setattr(self, k, v)

        self.__init_tags()
        self.details_populated = True
