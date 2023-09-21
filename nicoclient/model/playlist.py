from typing import List, Optional

from pydantic import BaseModel

from nicoclient.model.video import VideoThumbnail


class Playlist(BaseModel):
    id: str
    name: str
    owner_id: Optional[str]
    videos: List[VideoThumbnail]
    is_monitored: bool
