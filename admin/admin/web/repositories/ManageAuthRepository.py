from config.auth import AUTH


class ManageAuthRepository:
    @staticmethod
    def count():
        return AUTH['model'].count()

    @staticmethod
    def index(offset, items):
        return AUTH['model'] \
            .select(
                'id', 'name', 'email', 'permission', 'created_at',
                'updated_at'
            ) \
            .offset(offset) \
            .limit(items) \
            .get() \
            .serialize()

    @staticmethod
    def show(id):
        return AUTH['model'] \
            .find(id) \
            .serialize()

    @staticmethod
    def store(params):
        return AUTH['model'].insert(**params)

    @staticmethod
    def update(id, params):
        return AUTH['model'] \
            .where('id', id) \
            .update(**params)

    @staticmethod
    def destroy(id):
        return AUTH['model'].find(id).delete()

    @staticmethod
    def password_update(id, password):
        return AUTH['model'] \
            .where('id', id) \
            .update({'password': password})
