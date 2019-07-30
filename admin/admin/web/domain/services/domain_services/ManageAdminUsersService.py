from ....reositories.ManageAdminUsersRepository import \
    ManageAdminUsersRepository
from ...domain_models.ManageAdminUsersEntity import ManageAdminUsersEntity
from ..ApplicationService import ApplicationService


class ManageAdminUsersService:
    @staticmethod
    def store(params):
        params['password'] = f"{params['name']}_password"
        new_user = ManageAdminUsersEntity(**params).get_store_user()
        result = ManageAdminUsersRepository.store(new_user)
        return result

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

    @staticmethod
    def update(id, params):
        params = ApplicationService.delete_login_params(params)
        is_success = ManageAdminUsersRepository.update(id, params)
        return is_success
