from masonite.controllers import Controller
from masonite.request import Request
from masonite.response import Response
from masonite.helpers import config  #


class OptionsController:
     def options(self, request: Request, response: Response):
        headers = config('middleware.cors') or {}
        print(headers)
        response.make_headers(**headers)
        return response.json('', status=200)
