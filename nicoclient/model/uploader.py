from typing import List

from pydantic import BaseModel


class Uploader(BaseModel):
    id: str
    names: List[str]
