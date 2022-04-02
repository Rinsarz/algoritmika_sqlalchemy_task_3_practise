import falcon
from classic.components import component
from domain import services
from falcon import Request, Response

from .join_points import join_point


@component
class Note:
    service: services.NotesManager

    @join_point
    def on_get(self, request: Request, response: Response, note_id: int):
        note = self.service.get_note(note_id)

        context = {
            'header': note.header,
            'author': note.author.name,
            'text': note.text,
            'tags': [tag.name for tag in note.tags],
            'likes': note.likes,
            'created_date': note.created_date.strftime("%Y-%m-%d %H:%M:%S"),
            'modified_date': note.modified_date.strftime("%Y-%m-%d %H:%M:%S"),
        }

        response.media = context
        response.status = falcon.HTTP_200

    @join_point
    def on_put(self, request: Request, response: Response, note_id: int):
        updated_note = request.media

        if 'id' not in updated_note:
            updated_note['id'] = note_id

        self.service.update_note(**updated_note)

        context = {
            'message': 'Note successfully modified'
        }
        response.media = context
        response.status = falcon.HTTP_200

    @join_point
    def on_patch(self, request: Request, response: Response, note_id: int):
        patched_note = request.media

        if 'id' not in patched_note:
            patched_note['id'] = note_id

        self.service.partially_update(**patched_note)
        context = {
            'message': 'Note successfully modified'
        }
        response.media = context
        response.status = falcon.HTTP_200

    @join_point
    def on_delete(self, request: Request, response: Response, note_id: int):
        self.service.delete_note(note_id)
        context = {
            'message': 'Note successfully deleted'
        }
        response.media = context
        response.status = falcon.HTTP_200


@component
class Notes:
    service: services.NotesManager

    @join_point
    def on_get(self, request: Request, response: Response):
        limit = request.get_param_as_int('limit') or 50
        offset = request.get_param_as_int('offset') or 0

        request.params['limit'] = limit
        request.params['offset'] = offset

        notes = self.service.get_notes_with_filters(request.params)

        if not notes:
            context = {
                'message': 'Note(s) not found'
            }
        else:
            context = [
                {
                    'header': note.header,
                    'author': note.author.name,
                    'text': note.text,
                    'tags': [tag.name for tag in note.tags],
                    'likes': note.likes,
                    'created_date': note.created_date.strftime("%Y-%m-%d %H:%M:%S"),
                    'modified_date': note.modified_date.strftime("%Y-%m-%d %H:%M:%S"),
                } for note in notes
            ]

        response.media = context
        response.status = falcon.HTTP_200

    @join_point
    def on_post(self, request: Request, response: Response):
        self.service.create_note(**request.media)
        context = {
            'message': 'Note successfully created'
        }
        response.media = context
        response.status = falcon.HTTP_201
