import json

VIDEO_TYPE_UTATTEMITA = 'utattemita'
VIDEO_TYPE_VOCALOID_ORG = 'org'
VIDEO_TYPE_UNKNOWN = 'unknown'


class Video:
    def __init__(self, id=None, url=None, views=None, likes=None):
        self.id = None
        self.views = views
        self.likes = likes
        self.thumbnail_url = None
        self.title = None

        if (1 if url else 0) + (1 if id else 0) != 1:
            raise AssertionError("'id' or 'url' needed.")

        if url:
            self.id = url.split('/')[-1].split('?')[0]
        if id:
            self.id = id

    def __str__(self):
        return json.dumps(self.__dict__)
