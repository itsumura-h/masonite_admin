from config.auth import AUTH


class AdminUsersRepository:
    @staticmethod
    def index():
        return AUTH['model'] \
            .select('id', 'name', 'email', 'permission','created_at', 'updated_at') \
            .get() \
            .serialize()
