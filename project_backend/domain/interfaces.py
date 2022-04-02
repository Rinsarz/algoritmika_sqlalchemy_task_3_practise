from abc import ABC, abstractmethod
from typing import (
    List,
    Optional,
    Set,
    Union
)

from .my_dataclasses import (
    Authors,
    Notes,
    Tags,
    TagsToNotes
)


class NotesRepo(ABC):
    @abstractmethod
    def get_filtered_notes(self, filter_query: List) -> Optional[List[Notes]]:
        ...

    @abstractmethod
    def get_by_id(self, note_id: int) -> Optional[Notes]:
        ...

    @abstractmethod
    def get_by_text_filter(self, field_name: str, filter_flag: str, filter_value: str) -> Optional[List[Notes]]:
        ...

    @abstractmethod
    def get_by_numbers_filter(self, field_name: str, filter_flag: str, filter_value: str) -> Optional[List[Notes]]:
        ...

    @abstractmethod
    def add_instance(self, note: Notes) -> Notes:
        ...

    @abstractmethod
    def delete_instance(self, note: Notes):
        ...


class TagsRepo(ABC):
    @abstractmethod
    def get_by_id(self, tag_id: int) -> Optional[Tags]:
        ...

    @abstractmethod
    def get_by_name(self, tag_names: Set[Union[str, Tags]]) -> List[Tags]:
        ...

    @abstractmethod
    def add_instance(self, tag: Tags) -> Tags:
        ...


class AuthorsRepo(ABC):
    @abstractmethod
    def get_by_id(self, author_id: int) -> Optional[Authors]:
        ...

    @abstractmethod
    def get_by_name(self, author_name: str) -> Optional[Authors]:
        ...

    @abstractmethod
    def add_instance(self, author: Authors) -> Authors:
        ...


class TagsToNotesRepo(ABC):
    @abstractmethod
    def get_by_note_id(self, note_id: int) -> Optional[List[TagsToNotes]]:
        ...

    @abstractmethod
    def add_instance(self, new_tag_to_note: TagsToNotes) -> TagsToNotes:
        ...
