# nicoclient

[![codecov](https://codecov.io/gh/jaeseopark/nicoclient/branch/master/graph/badge.svg)](https://codecov.io/gh/jaeseopark/nicoclient) ![PyPI](https://img.shields.io/pypi/v/nicoclient.svg)

A python client to interact with [nicovideo.jp](https://nicovideo.jp).

## Installation

```bash
pip install nicoclient
```

## Features

### Get metadata

```python
metadata = nicoclient.get_metadata('sm34734479')
print(json.dumps(metadata, indent=2, ensure_ascii=False))
```

```json
{
  "id": "sm34734479",
  "views": 3033,
  "likes": 163,
  "thumbnail_url": "http://tn.smilevideo.jp/smile?i=34734479.81262",
  "title": "出来るだけ感情的に「ヘイトクライム」を歌いました。",
  "uploader_id": "33765098",
  "tags": [
    "歌ってみた",
    "ヘイトクライム(さまぐら)",
    "さまぐら",
    "檀上大空",
    "みけ（歌い手）",
    "ててて",
    "ボカロオリジナルを歌ってみた"
  ],
  "description": "最後まで聴いてもらえると嬉しいです。素晴らしい原曲  sm33841308MIX　みけ　mylist/58924781　https://twitter.com/rnike_san 歌　ててて　mylist/41403147　https://twitter.com/tetete2525"
}
```

### Get trending videos

```python
videos = nicoclient.get_trending_videos()
for video in videos:
    print(f"'{video['id']}' has {video['views']} views and {video['likes']} likes")
```
```
'sm34658459' has 40057 views and 1293 likes
'sm34248511' has 278194 views and 14274 likes
'sm34676260' has 96529 views and 6554 likes
...
```

### Get videos in a playlist

```python
videos = nicoclient.get_videos_by_playlist_id('58924781')
for video in videos:
    print(f"'{video['id']}' has {video['views']} views and {video['likes']} likes")
```
```
'sm29118726' has 1104 views and 28 likes
'sm29299741' has 837 views and 19 likes
'sm29816849' has 1476 views and 32 likes
...
```

### Get related videos

#### Use case 1

If the video is a Vocaloid Original, then the function returns Utattemita videos.

```python
related_videos = nicoclient.get_related_videos('sm32076378')
print('\n'.join([v['title'] for v in related_videos]))
```
```
"ドラマツルギー 歌ってみた【りぶ】",
"ドラマツルギー　歌ってみた【そらる】",
"【ウォルピス社】ドラマツルギーを歌ってみました【提供】",
"【浦島坂田船歌ってみたツアー】ドラマツルギー【うらたぬき】",
"【爽快に】ドラマツルギー 歌ってみた ver.Sou",
"『ドラマツルギー』を 歌ってみた。by天月",
...
```

#### Use case 2

If the video is _NOT_ a Vocaloid Original, then the function returns other videos by the uploader.

```python
related_videos = nicoclient.get_related_videos('sm32103696')
print('\n'.join([v['title'] for v in related_videos]))
```
```
"Marygold 歌ってみた【りぶ】",
"沙上の夢喰い少女 歌ってみた【りぶ】",
"BEAUTIFUL DREAMER 歌ってみた【りぶ】",
"夜と虹色 歌ってみた【りぶ】",
"Starduster 歌ってみた【りぶ】",
"ピエロ 歌ってみた【りぶ】",
...
```
