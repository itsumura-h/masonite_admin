from admin.web.AdminUsers.AdminUsersRepository import AdminUsersRepository
from admin.web.AdminUsers.AdminUsersEntity import AdminUserEntity

from pprint import pprint

class AdminUsersService:
    @staticmethod
    def index():
        admin_users = AdminUsersRepository.index()
        admin_users = [AdminUserEntity(**val) for val in admin_users]
        return admin_users
