from masonite.helpers import password as bcrypt_password

from config.auth import AUTH


class ManageAdminUsersRepository:
    @staticmethod
    def count():
        return AUTH['model'].count()

    @staticmethod
    def create(params):
        new_user = AUTH['model']()
        for key, value in params.items():
            setattr(new_user, key, value)
        new_user.save()
        return new_user

    @staticmethod
    def index(offset, items):
        return AUTH['model'] \
            .select('id', 'name', 'email', 'permission', 'created_at', 'updated_at') \
            .offset(offset) \
            .limit(items) \
            .get() \
            .serialize()

    @staticmethod
    def show(id):
        return AUTH['model'] \
            .find(id) \
            .serialize()
