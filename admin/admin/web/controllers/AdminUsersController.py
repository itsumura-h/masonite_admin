from masonite.request import Request
from masonite.response import Response

from admin.web.AdminUsers.AdminUsersService import AdminUsersService
from admin.web.ApplicationService import ApplicationService


class AdminUsersController:
    def create(self, request: Request, response: Response):
        params = request.all()
        params = ApplicationService.delete_login_params(params)
        result = AdminUsersService.create(params)
        if isinstance(result, str):
            return response.json(result, status=400)
        else:
            return result

    def index(self, request: Request):
        # pagenagion
        items = int(request.input('i')) if request.input('i') else 10
        page = int(request.input('p')) if request.input('p') else 1
        offset = items * (page - 1)

        admin_users, count = AdminUsersService.index(offset, items)
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
        admin_user = AdminUsersService.show(id)
        return {
            'id': admin_user.id,
            'name': admin_user.name,
            'email': admin_user.email,
            'permission': admin_user.permission.get_label(),
            'created_at': admin_user.created_at,
            'updated_at': admin_user.updated_at
        }