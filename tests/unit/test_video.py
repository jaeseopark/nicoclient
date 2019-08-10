import unittest

from nicoclient.model.video import Video


class TestVideo(unittest.TestCase):
    def test_find_references(self):
        video = Video(id='fake_id')
        video.description = "本家様【sm31229321】\n◆ Vocal：みけ( mylist/58924781 ) @rnike_san\n◆ Mix：藤( mylist/58622226 )@fujimameo\n◆Enc：らふどん(user/1896533)　@rfdn_0117"
        refs = video.find_references()
        self.assertEqual('sm31229321', refs[0])
        self.assertEqual('mylist/58924781', refs[1])
        self.assertEqual('mylist/58622226', refs[2])
