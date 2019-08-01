from masonite.helpers import config  # 
from masonite.request import Request
from masonite.response import Response


class OptionsController:
    def options(self, request: Request, response: Response):
        headers = config('middleware.cors') or {}
        print(headers)
        response.make_headers(**headers)
        return response.json('', status=200)
