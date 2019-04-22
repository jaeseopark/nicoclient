# nico_client

A python client to interact with [nicovideo.jp](https://nicovideo.jp).

## Features

### Get daily trending videos

```python
videos = nico_client.get_daily_trending_videos()

for video in videos:
    print(f"'{video.id}' has {video.views} views and {video.likes} likes")

# 'sm34658459' has 40057 views and 1293 likes
# 'sm34248511' has 278194 views and 14274 likes
# 'sm34676260' has 96529 views and 6554 likes
# ...
```

### Get video info

```python
video = Video(id='sm34734479')

nico_client.populate_details(video)
print(video)

# {
#   "id": "sm34734479",
#   "views": 3033,
#   "likes": 163,
#   "thumbnail_url": "http://tn.smilevideo.jp/smile?i=34734479.81262",
#   "title": "出来るだけ感情的に「ヘイトクライム」を歌いました。",
#   "tags": [
#     "歌ってみた",
#     "ヘイトクライム(さまぐら)",
#     "さまぐら",
#     "檀上大空",
#     "みけ（歌い手）",
#     "ててて",
#     "ボカロオリジナルを歌ってみた"
#   ],
#   "description": "最後まで聴いてもらえると嬉しいです。素晴らしい原曲  sm33841308MIX　みけ　mylist/58924781　https://twitter.com/rnike_san 歌　ててて　mylist/41403147　https://twitter.com/tetete2525",
#   "uploader_id": "33765098",
#   "details_populated": true,
#   "video_type": "utattemita"
# }
```

### Get related videos

Videos that have similar titles and the videos from same playlist

```python
video = Video(id='sm34734479')

related_videos = nico_client.get_related_videos(video)

# Output TBD
```

### Get videos in a playlist

```python
videos = nico_client.get_videos_by_playlist_id('58924781')

for video in videos:
    print(f"'{video.id}' has {video.views} views and {video.likes} likes")

# Output TBD
```

## Tests

### Run tests by scope

```bash
# TEST_SCOPE is a comma-separated list
export TEST_SCOPE=unit,integration

python3 -m unittest discover
```

Note: if `TEST_SCOPE` isn't provided, then it runs all tests.
