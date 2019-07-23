from masonite.request import Request
from masonite.response import Response

from admin.web.AdminUsers.AdminUsersService import AdminUsersService


class AdminUsersController:
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
                    'permission': val.permission,
                    'created_at': val.created_at,
                    'updated_at': val.updated_at
                } for val in admin_users
            ]
        }
