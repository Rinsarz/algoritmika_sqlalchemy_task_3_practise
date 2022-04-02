from typing import List, Optional, Set, Union

from classic.components import component
from classic.sql_storage import BaseRepository
from domain import interfaces
from domain.my_dataclasses import (
    Authors,
    Notes,
    Tags,
    TagsToNotes
)
from sqlalchemy import and_


@component
class NotesRepo(BaseRepository, interfaces.NotesRepo):
    def get_filtered_notes(self, filter_query: List) -> Optional[List[Notes]]:
        return self.session.query(Notes).filter(and_(*filter_query)).all()

    def get_by_id(self, note_id: int) -> Optional[Notes]:
        return self.session.query(Notes).filter_by(id=note_id).one_or_none()

    def get_by_text_filter(self, field_name: str, filter_flag: str, filter_value: str):
        filters = {
            'like': getattr(Notes, field_name).like(f'%{filter_value}%'),
            'eq': getattr(Notes, field_name) == filter_value,
        }
        return filters.get(filter_flag)

    def get_by_numbers_filter(self, field_name: str, filter_flag: str, filter_value: str):
        filters = {
            'gt': getattr(Notes, field_name) > filter_value,
            'gte': getattr(Notes, field_name) >= filter_value,
            'lt': getattr(Notes, field_name) < filter_value,
            'lte': getattr(Notes, field_name) <= filter_value,
        }
        return filters.get(filter_flag)

    def add_instance(self, note: Notes) -> Notes:
        self.session.add(note)
        self.session.flush()
        self.session.refresh(note)
        return note

    def delete_instance(self, note: Notes):
        self.session.delete(note)
        self.session.flush()


@component
class TagsRepo(BaseRepository, interfaces.TagsRepo):
    def get_by_id(self, tag_id: int) -> Optional[Tags]:
        return self.session.query(Tags).filter_by(id=tag_id).one_or_none()

    def get_by_name(self, tag_names: Set[Union[str, Tags]]) -> List[Tags]:
        return self.session.query(Tags).filter(Tags.name.in_(tag_names)).all()

    def add_instance(self, tag: Tags):
        self.session.add(tag)
        self.session.flush()
        self.session.refresh(tag)
        return tag


@component
class AuthorsRepo(BaseRepository, interfaces.AuthorsRepo):
    def get_by_id(self, author_id: int) -> Optional[Authors]:
        return self.session.query(Authors).filter_by(id=author_id).one_or_none()

    def get_by_name(self, author_name: str) -> Optional[Authors]:
        return self.session.query(Authors).filter_by(name=author_name).one_or_none()

    def add_instance(self, author: Authors):
        self.session.add(author)
        self.session.flush()
        self.session.refresh(author)
        return author


@component
class TagsToNotesRepo(BaseRepository, interfaces.TagsToNotesRepo):
    def get_by_note_id(self, note_id: int) -> Optional[List[TagsToNotes]]:
        return self.session.query(TagsToNotes).filter_by(note_id=note_id).all()

    def add_instance(self, new_tag_to_note: TagsToNotes) -> TagsToNotes:
        self.session.add(new_tag_to_note)
        self.session.flush()
        self.session.refresh(new_tag_to_note)
        return new_tag_to_note
