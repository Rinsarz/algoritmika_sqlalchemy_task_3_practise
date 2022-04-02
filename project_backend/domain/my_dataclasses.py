from dataclasses import dataclass, field
from datetime import datetime
from typing import (
    List,
    Optional,
    Union
)


@dataclass
class Tags:
    name: str
    id: Optional[int] = None


@dataclass
class Authors:
    name: str
    id: Optional[int] = None


@dataclass
class Notes:
    header: str
    text: str
    author: Authors
    tags: List[Union[str, Tags]] = field(default_factory=List)
    id: Optional[int] = None
    likes: Optional[int] = None
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None


@dataclass
class TagsToNotes:
    tag_id: Tags
    note_id: Notes
