import secrets
from datetime import datetime

from config.admin import LOGIN_CONF
from admin.web.Login.LoginRepository import LoginRepository

token_path = 'databases/login.bin'


class LoginService:
    def __init__(self):
        self.token_path = LOGIN_CONF['file_path'] \
            if 'file_path' in LOGIN_CONF else token_path

    def login(self, login_id: int, permission: int):
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

    def logout(self, login_id: int):
        data = LoginRepository().load()
        data.pop(login_id)
        LoginRepository().dump(data)
