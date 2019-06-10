import os, pickle, io, secrets
from datetime import datetime

from config.admin import LOGIN_CONF

token_path = 'databases/login.bin'

class LoginToken:
    def __init__(self):
        self.token_path = LOGIN_CONF['file_path'] if 'file_path' in LOGIN_CONF else token_path

    def load(self):
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as f:
                return pickle.load(f)
        else:
            return {}

    def dump(self, data):
        with open(self.token_path, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    def login(self, login_id: int):
        hash = secrets.token_urlsafe()
        data = self.load()
        data[login_id] = {
            'token': hash,
            'last_access': datetime.now()
        }
        self.dump(data)
        return hash

    def update_last_access(self, login_id: int):
        data = self.load()
        data[login_id]['last_access'] = datetime.now()
        self.dump(data)

    def logout(self, login_id: int):
        data = self.load()
        data.pop(login_id)
        self.dump(data)
