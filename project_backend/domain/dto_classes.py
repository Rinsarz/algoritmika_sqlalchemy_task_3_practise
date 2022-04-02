from datetime import datetime
from typing import (
    Optional,
    Set,
    Union
)

from classic.app import DTO
from .my_dataclasses import Tags


class NoteInfo(DTO):
    header: str
    text: str
    author: str
    tags: Set[Union[str, Tags]] = None


class NoteInfoForChange(DTO):
    id: int
    modified_date: Optional[datetime] = None
    header: Optional[str] = None
    text: Optional[str] = None
    tags: Set[Union[str, Tags]] = None


class TagInfo(DTO):
    name: str


class AuthorInfo(DTO):
    name: str


class TagToNoteInfo(DTO):
    tag_id: int
    note_id: int
