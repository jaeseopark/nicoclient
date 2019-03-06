import json

VIDEO_TYPE_UTATTEMITA = 'utattemita'
VIDEO_TYPE_VOCALOID_ORG = 'org'
VIDEO_TYPE_UNKNOWN = 'unknown'


class Video(object):
    def __init__(self, id=None, url=None, views=None, likes=None, *args, **kwargs):
        self.id = id
        self.views = views
        self.likes = likes
        self.thumbnail_url = None
        self.title = None

        if url and self.id is None:
            self.id = url.split('/')[-1].split('?')[0]

    def __str__(self):
        return json.dumps(self.__dict__)
