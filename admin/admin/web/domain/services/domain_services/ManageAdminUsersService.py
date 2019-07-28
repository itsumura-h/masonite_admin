from ....reositories.ManageAdminUsersRepository import \
    ManageAdminUsersRepository
from ...domain_models.ManageAdminUsersEntity import ManageAdminUsersEntity


class ManageAdminUsersService:
    @staticmethod
    def create(params):
        new_user = ManageAdminUsersEntity(**params).new()
        try:
            result = ManageAdminUsersRepository.create(new_user)
        except Exception as e:
            return str(e)
        return result.id

    @staticmethod
    def index(offset, items):
        admin_users = ManageAdminUsersRepository.index(offset, items)
        admin_users = [ManageAdminUsersEntity(**val) for val in admin_users]

        count = ManageAdminUsersRepository.count()

        return admin_users, count

    @staticmethod
    def show(id):
        admin_user = ManageAdminUsersRepository.show(id)
        admin_user = ManageAdminUsersEntity(**admin_user)
        return admin_user