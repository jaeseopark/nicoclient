# nico_client

A python client to interact with [nicovideo.jp](https://nicovideo.jp).

## Features

### Get daily trending videos

```python
client = NicoClient()
videos = client.get_daily_trending_videos()

for video in videos:
    print(f"'{video.video_id}' has {video.views} views and {video.likes} likes")
```

Output
```bash
'sm34658459' has 40057 views and 1293 likes
'sm34248511' has 278194 views and 14274 likes
'sm34676260' has 96529 views and 6554 likes
...
```

## Tests

### Run all tests

```bash
python3 -m unittest discover
```

### Run a specific test module/class

Example
```bash
python3 -m unittest tests.unit.test_daily_trending 
``` 