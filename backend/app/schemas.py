from pydantic import BaseModel
from typing import List, Optional

class ChapterBase(BaseModel):
    number: int
    name: str

class ChapterCreate(ChapterBase):
    content: str

class ChapterListResponse(ChapterBase):
    """Chapter without content for lists."""
    id: int

    class Config:
        from_attributes = True

class ChapterResponse(ChapterListResponse):
    """Full chapter with content."""
    content: str

class TitleBase(BaseModel):
    name: str
    author: str
    description: str

class TitleCreate(TitleBase):
    cover_url: Optional[str] = None  # Added optional cover

class TitleResponse(TitleBase):
    id: int
    cover_url: Optional[str] = None
    chapters: List[ChapterListResponse] = []  # Use list schema without content

    class Config:
        from_attributes = True