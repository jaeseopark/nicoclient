from nicopy import nicopy


def get_video_info(id):
    video_info = nicopy.get_video_info(video_id=id)
    return {
        'tags': [tag['tag'] for tag in video_info.get('tags')],
        'description': video_info.get('description'),
        'uploader_id': video_info.get('user_id'),
        'title': video_info.get('title'),
        'thumbnail_url': video_info.get('thumbnail_url'),
        'views': int(video_info.get('view_counter')),
        'likes': int(video_info.get('mylist_counter'))
    }


