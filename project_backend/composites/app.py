from adapters import api, database
from classic.sql_storage import TransactionContext
from domain import services
from sqlalchemy import create_engine


class Settings:
    db = database.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.METADATA.create_all(engine)

    context = TransactionContext(bind=engine, expire_on_commit=False)

    notes_repo = database.repositories.NotesRepo(context=context)
    tags_repo = database.repositories.TagsRepo(context=context)
    authors_repo = database.repositories.AuthorsRepo(context=context)
    tags_to_notes_repo = database.repositories.TagsToNotesRepo(context=context)


class Application:
    notes = services.NotesManager(
        notes_repo=DB.notes_repo,
        tags_repo=DB.tags_repo,
        authors_repo=DB.authors_repo,
        tags_to_notes_repo=DB.tags_to_notes_repo,
    )


class Aspects:
    services.join_points.join(DB.context)
    api.join_points.join(DB.context)


app = api.create_app(
    notes_service=Application.notes,
)
