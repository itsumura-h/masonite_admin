from masonite.helpers import password as bcrypt_password


class PermissionValueObject:
    def __init__(self, value):
        if value == '1' or value == '2' or value == '3':
            self.__init_by_db(value)
        else:
            self.__init_by_request(value)

    def __init_by_db(self, value):
        self.value = int(value)

    def __init_by_request(self, value):
        if value == 'administrator':
            self.value = 1
        elif value == 'member':
            self.value = 2
        elif value == 'user':
            self.value = 3

    def get_label(self):
        if self.value == 1:
            return 'administrator'
        elif self.value == 2:
            return 'member'
        elif self.value == 3:
            return 'user'


class PasswordValueObject:
    def __init__(self, value):
        self.__value = value

    def get_hashed_value(self):
        return bcrypt_password(self.__value)


class ManageAdminUsersEntity:
    def __init__(self, id: int = None, name: str = None, email: str = None,
                 password: str = None, permission=None, created_at: str = None,
                 updated_at: str = None):
        self.id = id
        self.name = name
        self.email = email
        self.password = PasswordValueObject(password)
        self.permission = PermissionValueObject(permission)
        self.created_at = created_at
        self.updated_at = updated_at

    def get_store_user(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password.get_hashed_value(),
            'permission': self.permission.value
        }
