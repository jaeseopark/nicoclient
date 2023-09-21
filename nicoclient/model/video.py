from typing import Optional

from pydantic import BaseModel


class Video(BaseModel):
    id: str
    title: str
    views: int
    likes: int
    duration: int  # seconds
    is_accessible: bool
    timestamp: int  # epoch format
    thumbnail_url: str = None
    parent_video_id: Optional[str] = None
    description: Optional[str] = None
