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


class HashPasswordValueObject:
    def __init__(self, value):
        if value:
            self.value = bcrypt_password(value)
        else:
            self.value = None

    def get_value(self):
        return self.value


class ManageAdminUsersEntity:
    def __init__(self, id: int = None, name: str = None, email: str = None,
                 password: str = None, permission=None, created_at: str = None,
                 updated_at: str = None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.hash_password = HashPasswordValueObject(password).get_value()
        self.permission = PermissionValueObject(permission)
        self.created_at = created_at
        self.updated_at = updated_at

    def new(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.hash_password,
            'permission': self.permission.value
        }
