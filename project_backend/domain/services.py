import datetime
from typing import List, Optional, Union

from classic.app import validate_with_dto
from classic.aspects import PointCut
from classic.components import component
from pydantic import validate_arguments

from . import interfaces
from .my_dataclasses import (
    Authors,
    Notes,
    Tags
)
from .dto_classes import (
    AuthorInfo,
    NoteInfo,
    NoteInfoForChange,
    TagInfo
)
from .errors import FindByIdError, FilterKeyError

join_points = PointCut()
join_point = join_points.join_point


@component
class NotesManager:
    notes_repo: interfaces.NotesRepo
    tags_repo: interfaces.TagsRepo
    authors_repo: interfaces.AuthorsRepo
    tags_to_notes_repo: interfaces.TagsToNotesRepo

    def get_tags(self, note_id: int) -> List[str]:
        current_tags = []
        tags = self.tags_to_notes_repo.get_by_note_id(note_id)
        for tag in tags:
            tag = self.get_tag(tag.tag_id)
            current_tags.append(tag.name)
        return current_tags

    def get_tag(self, tag_id: int) -> Tags:
        tag = self.tags_repo.get_by_id(tag_id)

        if tag is None:
            raise FindByIdError()

        return tag

    def modify_note_info_by_author(self, note_info: Union[NoteInfo, NoteInfoForChange]) -> \
            Union[NoteInfo, NoteInfoForChange]:
        author_check = self.authors_repo.get_by_name(note_info.author)

        if author_check is None:
            author_info = AuthorInfo(name=note_info.author)
            new_author = author_info.create_obj(Authors)
            author = self.authors_repo.add_instance(new_author)
            note_info.author = author
        else:
            note_info.author = author_check
        return note_info

    def modify_note_info_by_tags(self, note_info: Union[NoteInfo, NoteInfoForChange]) -> \
            Union[NoteInfo, NoteInfoForChange]:

        db_tags = self.tags_repo.get_by_name(note_info.tags)
        db_tags_names = {tag.name for tag in db_tags}

        new_tags = note_info.tags - db_tags_names
        note_info.tags = note_info.tags - new_tags
        note_info.tags = [tag for tag in db_tags]

        for tag_name in new_tags:
            tag_info = TagInfo(name=tag_name)
            new_tag = tag_info.create_obj(Tags)
            tag = self.tags_repo.add_instance(new_tag)
            note_info.tags.append(tag)

        return note_info

    @join_point
    @validate_with_dto
    def create_note(self, note_info: NoteInfo):

        note_info = self.modify_note_info_by_author(note_info)

        note_info = self.modify_note_info_by_tags(note_info)

        new_note = note_info.create_obj(Notes)

        new_note.created_date = datetime.datetime.now()
        new_note.modified_date = datetime.datetime.now()

        self.notes_repo.add_instance(new_note)

    @join_point
    @validate_arguments
    def get_note(self, note_id: int) -> Notes:
        note = self.notes_repo.get_by_id(note_id)

        if note is None:
            raise FindByIdError()

        return note

    @join_point
    @validate_arguments
    def get_notes_with_filters(self, query: dict) -> Optional[List[Notes]]:
        notes = self.filter_notes(query)

        return notes

    @join_point
    @validate_arguments
    def filter_notes(self, query: dict) -> Optional[List[Notes]]:
        filter_query = []

        header_filter = query.get('header')
        if header_filter is not None:
            flag, value = self.parse_filter_values(header_filter)
            filter_query.append(self.filter_by_text_filters('header', flag, value))

        text_filter = query.get('text')
        if text_filter is not None:
            flag, value = self.parse_filter_values(text_filter)
            filter_query.append(self.filter_by_text_filters('text', flag, value))

        likes_filters = query.get('likes')
        if likes_filters is not None:
            flag, value = self.parse_filter_values(likes_filters)
            filter_query.append(self.filter_by_numbers_filters('likes', flag, value))

        notes = self.notes_repo.get_filtered_notes(filter_query)

        tags_filters = query.get('tags')
        if tags_filters is not None:
            tags_filters = {el for el in tags_filters.split(',')}

            filtered_by_tags_notes = []

            for note in notes:
                note_tags_names = {tag.name for tag in note.tags}
                if len(tags_filters & note_tags_names) != 0:
                    filtered_by_tags_notes.append(note)

            notes = filtered_by_tags_notes

        limit = query.get('limit')
        offset = query.get('offset')

        return notes[offset: limit + offset]

    @staticmethod
    def parse_filter_values(filter_value: str) -> List[str]:
        return filter_value.split(':')

    def filter_by_text_filters(self, field_name: str, filter_flag: str, filter_value: str):
        filter_query = self.notes_repo.get_by_text_filter(field_name, filter_flag, filter_value)

        if filter_query is None:
            raise FilterKeyError()

        return filter_query

    def filter_by_numbers_filters(self, field_name: str, filter_flag: str, filter_value: str):
        filter_query = self.notes_repo.get_by_numbers_filter(field_name, filter_flag, filter_value)

        if filter_query is None:
            raise FilterKeyError()

        return filter_query

    @join_point
    @validate_arguments
    def delete_note(self, note_id: int):
        note = self.get_note(note_id)

        self.notes_repo.delete_instance(note)

    @join_point
    @validate_with_dto
    def update_note(self, note_info: NoteInfoForChange):
        note = self.get_note(note_info.id)

        note_info.modified_date = datetime.datetime.now()

        note_info = self.modify_note_info_by_tags(note_info)

        note_info.populate_obj(note)

    @join_point
    @validate_with_dto
    def partially_update(self, note_info: NoteInfoForChange):

        old_note_data = self.get_note(note_info.id)

        if note_info.header is None:
            note_info.header = old_note_data.header
        if note_info.text is None:
            note_info.text = old_note_data.text

        old_note_data.modified_date = datetime.datetime.now()

        note_info = self.modify_note_info_by_tags(note_info)

        note_info.populate_obj(old_note_data)
