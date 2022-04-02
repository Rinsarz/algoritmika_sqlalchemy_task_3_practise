from domain import my_dataclasses
from sqlalchemy.orm import registry, relationship

from . import tables

mapper = registry()

mapper.map_imperatively(
    my_dataclasses.Notes,
    tables.NOTES_TABLE,
    properties={
        'tags': relationship(
            my_dataclasses.Tags,
            secondary=tables.TAGS_TO_NOTES_TABLE
        ),
    }
)

mapper.map_imperatively(
    my_dataclasses.Tags,
    tables.TAGS_TABLE
)

mapper.map_imperatively(
    my_dataclasses.Authors,
    tables.AUTHORS_TABLE,
    properties={
        'note': relationship(my_dataclasses.Notes, backref='author', uselist=True),
    }
)

mapper.map_imperatively(
    my_dataclasses.TagsToNotes,
    tables.TAGS_TO_NOTES_TABLE,
)
