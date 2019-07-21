from masonite.request import Request
from masonite.response import Response

from admin.web.AdminUsers.AdminUsersService import AdminUsersService


class AdminUsersController:
    def index(self, request: Request):
        admin_users = AdminUsersService.index()
        return [
            {
                'id': val.id,
                'name': val.name,
                'email': val.email,
                'permission': val.permission,
                'created_at': val.created_at,
                'updated_at': val.updated_at
            } for val in admin_users
        ]
