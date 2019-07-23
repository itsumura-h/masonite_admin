from admin.web.AdminUsers.AdminUsersRepository import AdminUsersRepository
from admin.web.AdminUsers.AdminUsersEntity import AdminUserEntity


class AdminUsersService:
    @staticmethod
    def create(params):
        new_user = AdminUserEntity(**params).new()
        try:
            result = AdminUsersRepository.create(new_user)
        except Exception as e:
            return str(e)
        return result.id


    @staticmethod
    def index(offset, items):
        admin_users = AdminUsersRepository.index(offset, items)
        admin_users = [AdminUserEntity(**val) for val in admin_users]

        count = AdminUsersRepository.count()

        return admin_users, count

    @staticmethod
    def show(id):
        admin_user = AdminUsersRepository.show(id)
        admin_user = AdminUserEntity(**admin_user)
        return admin_user