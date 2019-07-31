from ....reositories.ManageAuthRepository import \
    ManageAuthRepository
from ...domain_models.ManageAuthEntity import ManageAuthEntity
from ..ApplicationService import ApplicationService


class ManageAuthService:
    @staticmethod
    def index(offset, items):
        admin_users = ManageAuthRepository.index(offset, items)
        admin_users = [
            ManageAuthEntity(**val).get_index_dict()
            for val in admin_users
        ]

        count = ManageAuthRepository.count()

        return admin_users, count

    @staticmethod
    def show(id):
        admin_user = ManageAuthRepository.show(id)
        admin_user = ManageAuthEntity(**admin_user).get_show_dict()
        return admin_user

    @staticmethod
    def store(params):
        params['password'] = f"{params['name']}_password"
        new_user = ManageAuthEntity(**params).get_store_dict()
        result = ManageAuthRepository.store(new_user)
        return result

    @staticmethod
    def update(id, params):
        params = ApplicationService.delete_login_params(params)
        is_success = ManageAuthRepository.update(id, params)
        return is_success

    @staticmethod
    def destroy(id):
        return ManageAuthRepository.destroy(id)