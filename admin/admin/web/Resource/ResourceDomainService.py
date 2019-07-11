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
        self.model = model
        self.create_display = create_display
        self.list_display = list_display
        self.detail_display = detail_display

    def create(self, request: Request, response: Response):
        """Logic to create data from a given model."""
        if ResourceAppService().before_crud_check(request, response) is False:
            return response.json(None, status=403)

        try:
            params = request.all()
            del params['login_id'], params['login_token'], params['permission']
            new_model = self.model()

            ResourceRepository.create(params, new_model)
        except Exception as e:
            return {'error': str(e)}
        return new_model

    def index(self, request: Request, response: Response):
        """Logic to read data from several models."""
        if ResourceAppService().before_crud_check(request, response) is False:
            return response.json(None, status=403)

        # pagenagion
        items = int(request.input('i')) if request.input('i') else 10
        page = int(request.input('p')) if request.input('p') else 1
        offset = items * (page - 1)

        results = ResourceRepository.index(
            self.model, self.list_display, offset, items)
        return ResourceAppService().arr_iso_format(results)

    def count(self, request: Request, response: Response):
        if ResourceAppService().before_crud_check(request, response) is False:
            return response.json(None, status=403)

        return {'count': self.model.count()}

    def show(self, request: Request, response: Response):
        """Logic to read data from 1 model."""
        if ResourceAppService().before_crud_check(request, response) is False:
            return response.json(None, status=403)

        id = request.param('id')
        new_result = ResourceRepository.show(
            self.model,
            self.detail_display,
            id
        )

        return ResourceAppService().arr_iso_format(new_result)

    def update(self, request: Request, response: Response):
        """Logic to update data from a given model."""
        if ResourceAppService().before_crud_check(request, response) is False:
            return response.json(None, status=403)

        record = self.model.where('id', request.param('id'))
        params = request.all()
        del params['login_id'], params['login_token'], params['permission']

        try:
            record.update(params)
            ResourceRepository.update(record, params)
        except Exception as e:
            return {'error': str(e)}

        return {}

    def delete(self, request: Request, response: Response):
        """Logic to delete data from a given model."""
        if ResourceAppService().before_crud_check(request, response) is False:
            return response.json(None, status=403)

        id = request.param('id')
        result = ResourceRepository.delete(self.model, id)
        if result:
            return result
        else:
            return {'error': 'Record does not exist'}

    def options(self, request: Request, response: Response):
        headers = config('middleware.cors') or {}
        request.header(headers)
        return ''
