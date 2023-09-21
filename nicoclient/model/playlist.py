from typing import List, Optional

from pydantic import BaseModel

from nicoclient.model.video import Video


class Playlist(BaseModel):
    id: str
    name: str
    owner_id: Optional[str]
    videos: List[Video]
    is_monitored: bool
