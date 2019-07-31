from masonite.request import Request
from masonite.response import Response

from ..domain.services.domain_services.ManageAuthService import (
    ManageAuthService
)
from ..domain.services.ApplicationService import ApplicationService


class ManageAuthController:
    def index(self, request: Request):
        # pagenagion
        items = int(request.input('i')) if request.input('i') else 10
        page = int(request.input('p')) if request.input('p') else 1
        offset = items * (page - 1)

        admin_users, count = ManageAuthService.index(offset, items)
        return {
            'count': count,
            'admin_users': admin_users
        }

    def show(self, request: Request, response: Response):
        id = request.param('id')
        admin_user = ManageAuthService.show(id)
        return admin_user

    def store(self, request: Request, response: Response):
        try:
            params = request.all()
            params = ApplicationService.delete_login_params(params)
            ManageAuthService.store(params)
            return ''
        except Exception as e:
            return response.json({'error': str(e)}, status=400)

    def update(self, request: Request, response: Response):
        try:
            id = request.param('id')
            params = request.all()
            is_success = ManageAuthService.update(id, params)
            if is_success:
                return ''
        except Exception as e:
            return response.json({'error': str(e)}, status=400)

    def destroy(self, request: Request, response: Response):
        try:
            id = request.param('id')
            ManageAuthService.destroy(id)
            return ''
        except Exception as e:
            return response.json({'error': str(e)}, status=400)