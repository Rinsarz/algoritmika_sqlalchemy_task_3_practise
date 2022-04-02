from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table
)

METADATA = MetaData()

NOTES_TABLE = Table(
    'notes',
    METADATA,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('likes', Integer, default=0),
    Column('header', String(25)),
    Column('text', String(500)),
    Column('author_id', ForeignKey('authors.id', ondelete='CASCADE')),
    Column('created_date', DateTime, nullable=False),
    Column('modified_date', DateTime, nullable=False),
)

AUTHORS_TABLE = Table(
    'authors',
    METADATA,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(30), unique=True),
)

TAGS_TABLE = Table(
    'tags',
    METADATA,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(30), unique=True),
)

TAGS_TO_NOTES_TABLE = Table(
    'tags_to_notes',
    METADATA,
    Column('tag_id', ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    Column('note_id', ForeignKey('notes.id', ondelete='CASCADE'), primary_key=True),
)
