import json

import falcon
from falcon import Request, Response


class FindByIdError(Exception):
    @staticmethod
    def handle(req: Request, resp: Response, exc: 'FindByIdError', params: dict):
        resp.set_header('Error-Header', 'Error')
        resp.status = falcon.HTTP_404
        context = {'Error message': "Can't find record"}
        resp.text = json.dumps(context)


class FilterKeyError(Exception):
    @staticmethod
    def handle(req: Request, resp: Response, exc: 'FindByIdError', params: dict):
        resp.set_header('Error-Header', 'Error')
        resp.status = falcon.HTTP_404
        context = {'Error message': "Invalid filter"}
        resp.text = json.dumps(context)
