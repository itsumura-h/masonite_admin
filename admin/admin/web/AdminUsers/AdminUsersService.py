from admin.web.AdminUsers.AdminUsersRepository import AdminUsersRepository
from admin.web.AdminUsers.AdminUsersEntity import AdminUserEntity

from pprint import pprint

class AdminUsersService:
    @staticmethod
    def index(offset, items):
        admin_users = AdminUsersRepository.index(offset, items)
        admin_users = [AdminUserEntity(**val) for val in admin_users]

        count = AdminUsersRepository.count()

        return admin_users, count
