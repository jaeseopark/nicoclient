import json

VIDEO_TYPE_UTATTEMITA = 'utattemita'
VIDEO_TYPE_VOCALOID_ORG = 'org'
VIDEO_TYPE_UNKNOWN = 'unknown'


class Video:
    def __init__(self, video_id=None, url=None, views=None, likes=None):
        if url:
            self.video_id = url.split('/')[-1].split('?')[0]
        if video_id:
            self.video_id = video_id
        if not self.video_id:
            raise AssertionError("'video_id' or 'url' needed.")
        self.views = views
        self.likes = likes

    def __str__(self):
        return json.dumps(self.__dict__)
