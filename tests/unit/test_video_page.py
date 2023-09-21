import unittest

from nicoclient.html_page.video_page import VideoPage
from tests import get_file_content_as_string


class TestVideoPage(unittest.TestCase):
    def test_video_page_with_json_data(self):
        html_string = get_file_content_as_string('video_with_json.html')
        vp = VideoPage(html_string=html_string)
        self.assertTrue('他人の価値観なんて私は知らないの' in vp.video.description)
        self.assertEqual(401813, vp.video.views)
        self.assertEqual(5834, vp.video.likes)
        self.assertEqual('https://nicovideo.cdn.nimg.jp/thumbnails/10253831/10253831', vp.video.thumbnail_url)
        self.assertEqual('え？あぁ、そう。　歌ってみた－遊', vp.video.title)

    def test_video_page_without_json_data(self):
        html_string = get_file_content_as_string('video_without_json.html')
        vp = VideoPage(html_string=html_string)
        self.assertTrue('この楽曲が収録されているアルバム' in vp.video.description)
        self.assertEqual(118795, vp.video.views)
        self.assertEqual(2954, vp.video.likes)
        self.assertEqual('https://tn.smilevideo.jp/smile?i=24444796.L', vp.video.thumbnail_url)
        self.assertEqual('西へ行く buzzG feat.夏代孝明', vp.video.title)
