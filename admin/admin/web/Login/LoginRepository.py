import os
import pickle
from config.admin import LOGIN_CONF
from config.auth import AUTH

token_path = 'databases/login.bin'


class LoginRepository:
    def __init__(self):
        self.token_path = LOGIN_CONF['file_path'] if 'file_path' in LOGIN_CONF else token_path

    def get_user(self, email):
        return AUTH['model'].where('email', email).first().serialize()

    def load(self):
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as f:
                return pickle.load(f)
        else:
            return {}

    def dump(self, data):
        with open(self.token_path, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
