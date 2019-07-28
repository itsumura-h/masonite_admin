from masonite.request import Request
from masonite.response import Response

from ..domain.services.domain_services.ManageAdminUsersService import (
    ManageAdminUsersService
)
from ..domain.services.ApplicationService import ApplicationService


class ManageAdminUsersController:
    def create(self, request: Request, response: Response):
        params = request.all()
        params = ApplicationService.delete_login_params(params)
        result = ManageAdminUsersService.create(params)
        if isinstance(result, str):
            return response.json(result, status=400)
        else:
            return result

    def index(self, request: Request):
        # pagenagion
        items = int(request.input('i')) if request.input('i') else 10
        page = int(request.input('p')) if request.input('p') else 1
        offset = items * (page - 1)

        admin_users, count = ManageAdminUsersService.index(offset, items)
        return {
            'count': count,
            'admin_users': [
                {
                    'id': val.id,
                    'name': val.name,
                    'email': val.email,
                    'permission': val.permission.get_label(),
                    'created_at': val.created_at,
                    'updated_at': val.updated_at
                } for val in admin_users
            ]
        }

    def show(self, request: Request, response: Response):
        id = request.param('id')
        admin_user = ManageAdminUsersService.show(id)
        return {
            'id': admin_user.id,
            'name': admin_user.name,
            'email': admin_user.email,
            'permission': admin_user.permission.get_label(),
            'created_at': admin_user.created_at,
            'updated_at': admin_user.updated_at
        }

    def update(self, request:Request, response:Response):
        pass