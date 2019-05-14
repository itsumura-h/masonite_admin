from masonite.controllers import Controller
from masonite.request import Request
from config.auth import AUTH
from bcrypt import checkpw
from datetime import datetime
import hashlib

try:
    from app.models.LoginToken import LoginToken
except:
    from app.LoginToken import LoginToken

class LoginController(Controller):
    def store(self, request: Request):
        email = request.input('email')
        password = request.input('password')
        user = AUTH['model'].where('email', email).first()
        login = checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
        if login:
            # Delete existing token
            LoginToken.where('admin_user_id', user.id).delete()
            # hash = email + password + system time
            hash = user.email + user.password + str(datetime.now())
            hash = hashlib.sha1(hash.encode('utf-8')).hexdigest()

            login_token = LoginToken()
            login_token.admin_user_id = user.id
            login_token.token = hash
            result = login_token.save()
            return {'login': True, 'token': hash, 'id': user.id, 'name': user.name}
        else:
            return {'login': False}

    def destroy(self, request: Request):
        login_id = request.input('login_id')
        LoginToken.where('admin_user_id', login_id).delete()
        return {}