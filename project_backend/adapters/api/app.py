from classic.http_api import App
from domain import errors, services

from . import controllers


def create_app(
        notes_service: services.NotesManager,

) -> App:
    app = App()

    notes_controllers = controllers.Notes(service=notes_service)
    note_controllers = controllers.Note(service=notes_service)

    app.add_route('/notes/', notes_controllers)
    app.add_route('/notes/{note_id}', note_controllers)

    app.add_error_handler(errors.FindByIdError)
    app.add_error_handler(errors.FilterKeyError)

    return app
