from config.auth import AUTH


class AdminUsersRepository:
    @staticmethod
    def count():
        return AUTH['model'].count()

    @staticmethod
    def index(offset, items):
        return AUTH['model'] \
            .select('id', 'name', 'email', 'permission','created_at', 'updated_at') \
            .offset(offset) \
            .limit(items) \
            .get() \
            .serialize()
