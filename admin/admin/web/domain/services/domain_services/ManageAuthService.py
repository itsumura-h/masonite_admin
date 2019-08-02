from datetime import date

from bcrypt import checkpw
from masonite.helpers.password import password as make_password

from ....repositories.ManageAuthRepository import ManageAuthRepository
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
        params['password'] = \
            ApplicationService.generate_password(params['name'])
        new_user = ManageAuthEntity(**params).get_store_dict()
        ManageAuthRepository.store(new_user)
        return params['password']

    @staticmethod
    def update(id, params):
        params = ApplicationService.delete_login_params(params)
        is_success = ManageAuthRepository.update(id, params)
        new_user = ManageAuthRepository.show(id)
        new_user = ManageAuthEntity(**new_user).get_show_dict()
        return is_success, new_user

    @staticmethod
    def destroy(id):
        return ManageAuthRepository.destroy(id)

    @staticmethod
    def reset_password(id):
        name = ManageAuthRepository.show(id)['name']
        new_password = ApplicationService.generate_password(name)
        hash_password = make_password(new_password)
        ManageAuthRepository.password_update(id, hash_password)
        return new_password

    @staticmethod
    def update_password(id, password, new_password):
        # check Password
        old_hash_password = ManageAuthRepository.show(id)['password']
        is_success = checkpw(
            bytes(password, 'utf-8'),
            bytes(old_hash_password, 'utf-8')
        )

        if is_success:
            new_password = make_password(new_password)
            ManageAuthRepository.password_update(id, new_password)
        else:
            raise Exception('password invalid')
