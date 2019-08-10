import unittest

from nicoclient.html_page.video_page import VideoPage
from tests import get_file_content_as_string


class TestVideoPage(unittest.TestCase):
    def test_video_page_with_json_data(self):
        html_string = get_file_content_as_string('video_with_json.html')
        vp = VideoPage(html_string=html_string)
        info = vp.get_video_metadata()
        self.assertEqual(11, len(info['tags']))
        self.assertTrue('他人の価値観なんて私は知らないの' in info['description'])
        self.assertEqual(349705, info['views'])
        self.assertEqual(5850, info['likes'])
        self.assertEqual('https://tn.smilevideo.jp/smile?i=10253831', info['thumbnail_url'])
        self.assertEqual('4840929', info['uploader_id'])
        self.assertEqual('え？あぁ、そう。　歌ってみた－遊', info['title'])

    def test_video_page_with_json_data_english(self):
        html_string = get_file_content_as_string('video_with_json_eng.html')
        vp = VideoPage(html_string=html_string)
        info = vp.get_video_metadata()
        self.assertEqual(4, len(info['tags']))
        self.assertTrue('被害妄想携帯女子' in info['description'])
        self.assertEqual(1730597, info['views'])
        self.assertEqual(23360, info['likes'])
        self.assertEqual('https://tn.smilevideo.jp/smile?i=25445187', info['thumbnail_url'])
        self.assertEqual('8186836', info['uploader_id'])
        self.assertEqual('All Night, the Idea of Two Sang it【Natsushiro Takaaki and nqrse】', info['title'])

    def test_video_page_with_json_but_no_tags(self):
        html_string = get_file_content_as_string('video_with_json_but_no_tags.html')
        vp = VideoPage(html_string=html_string)
        info = vp.get_video_metadata()
        self.assertEqual(0, len(info['tags']))
        self.assertTrue('キワミパートでお借りした動画' in info['description'])
        self.assertEqual(462144, info['views'])
        self.assertEqual(11658, info['likes'])
        self.assertEqual('https://tn.smilevideo.jp/smile?i=8377121', info['thumbnail_url'])
        self.assertEqual('14219150', info['uploader_id'])
        self.assertEqual('【オールスター合作】ニコ色のオールスター流星群', info['title'])

    def test_video_page_without_json_data(self):
        html_string = get_file_content_as_string('video_without_json.html')
        vp = VideoPage(html_string=html_string)
        info = vp.get_video_metadata()
        self.assertEqual(11, len(info['tags']))
        self.assertTrue('この楽曲が収録されているアルバム' in info['description'])
        self.assertEqual(118795, info['views'])
        self.assertEqual(2954, info['likes'])
        self.assertEqual('https://tn.smilevideo.jp/smile?i=24444796.L', info['thumbnail_url'])
        self.assertEqual('8186836', info['uploader_id'])
        self.assertEqual('西へ行く buzzG feat.夏代孝明', info['title'])
