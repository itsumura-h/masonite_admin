import secrets
from datetime import datetime

from bcrypt import checkpw

from ....repositories.LoginRepository import LoginRepository
from ...domain_models.LoginEntity import LoginUserEntity


class LoginService:
    def store(self, email, password):
        user = LoginRepository().get_user(email)
        user = LoginUserEntity(**user).get_store_dict()

        # login check
        is_login = checkpw(
            bytes(password, 'utf-8'),
            bytes(user['password'], 'utf-8')
        )
        if is_login:
            hash = secrets.token_urlsafe()
            data = LoginRepository().load()
            data[user['id']] = {
                'token': hash,
                'last_access': datetime.now(),
                'permission': user['permission']
            }
            LoginRepository().dump(data)
            return hash, user
        else:
            raise Exception("Password didn't match")

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
