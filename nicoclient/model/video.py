from typing import Optional

from pydantic import BaseModel


class VideoThumbnail(BaseModel):
    id: str
    title: str
    views: int
    likes: int
    duration: int  # seconds
    is_accessible: bool
    timestamp: int  # epoch format
    thumbnail_url: str = None


class Video(VideoThumbnail):
    parent_video_id: Optional[str] = None
    description: str
