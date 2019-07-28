class PermissionValueObject:
    def __init__(self, value):
        if value == '1':
            value = 'administrator'
        elif value == '2':
            value = 'member'
        elif value == '3':
            value = 'user'

        self.value = value

    def get_value(self):
        return self.value


class LoginUserEntity:
    def __init__(self, id: int = None, name: str = None, email: str = None,
                 password: str = None, permission=None, created_at: str = None,
                 updated_at: str = None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.permission = PermissionValueObject(permission).get_value()
        self.created_at = created_at
        self.updated_at = updated_at
