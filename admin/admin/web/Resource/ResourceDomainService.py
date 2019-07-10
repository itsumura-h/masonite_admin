from datetime import date, datetime, time, timedelta
from app.http.middleware.AdminMiddleware import AdminMiddleware
from masonite.request import Request
from masonite.response import Response
from masonite import env
from admin.web.Resource.ResourceRepository import ResourceRepository
from admin.web.Resource.ResourceAppService import ResourceAppService
from masonite.helpers import config  #


class ResourceDomainService:
    # ==================================================
    # Domain Service
    # ==================================================

    def __init__(self, model=None, create_display=None, list_display=None, detail_display=None):
        self.resource_args = {
            'model': model,
            'create_display': create_display,
            'list_display': list_display,
            'detail_display': detail_display
        }

    def create(self, request: Request, response: Response):
        """Logic to create data from a given model."""
        if ResourceAppService().before_crud_check(request, response) is False:
            return response.json(None, status=403)

        return ResourceRepository(**self.resource_args).create(request, response)

    def index(self, request: Request, response: Response):
        """Logic to read data from several models."""
        if ResourceAppService().before_crud_check(request, response) is False:
            return response.json(None, status=403)

        return ResourceRepository(**self.resource_args).index(request, response)

    def count(self, request: Request, response: Response):
        if ResourceAppService().before_crud_check(request, response) is False:
            return response.json(None, status=403)

        return ResourceRepository(**self.resource_args).count(request, response)

    def show(self, request: Request, response: Response):
        """Logic to read data from 1 model."""
        if ResourceAppService().before_crud_check(request, response) is False:
            return response.json(None, status=403)

        return ResourceRepository(**self.resource_args).show(request, response)

    def update(self, request: Request, response: Response):
        """Logic to update data from a given model."""
        if ResourceAppService().before_crud_check(request, response) is False:
            return response.json(None, status=403)

        return ResourceRepository(**self.resource_args).update(request, response)

    def delete(self, request: Request, response: Response):
        """Logic to delete data from a given model."""
        if ResourceAppService().before_crud_check(request, response) is False:
            return response.json(None, status=403)

        return ResourceRepository(**self.resource_args).delete(request, response)

    def options(self, request: Request, response: Response):
        headers = config('middleware.cors') or {}
        request.header(headers)
        return ''
