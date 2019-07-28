import secrets
from datetime import datetime

# from config.admin import LOGIN_CONF

from ....reositories.LoginRepository import LoginRepository
from ...domain_models.LoginEntity import LoginUserEntity

# token_path = 'databases/login.bin'


class LoginService:
    # def __init__(self):
    #     self.token_path = LOGIN_CONF['file_path'] \
    #         if 'file_path' in LOGIN_CONF else token_path

    def get_user(self, email):
        user = LoginRepository().get_user(email)
        user = LoginUserEntity(**user)
        return user

    def login(self, login_id: int, permission: str):
        hash = secrets.token_urlsafe()
        data = LoginRepository().load()
        data[login_id] = {
            'token': hash,
            'last_access': datetime.now(),
            'permission': permission
        }
        LoginRepository().dump(data)
        return hash

    def update_last_access(self, login_id: int):
        data = LoginRepository().load()
        data[login_id]['last_access'] = datetime.now()
        LoginRepository().dump(data)

    def logout(self, id: int, token: str):
        data = LoginRepository().load()
        try:
            if data[id]['token'] == token:
                data.pop(id)
                LoginRepository().dump(data)
                return True
            else:
                raise Exception
        except Exception:
            return False
