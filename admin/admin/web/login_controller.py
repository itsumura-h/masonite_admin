import os, pickle, secrets
from datetime import datetime

from bcrypt import checkpw
from masonite.auth import Sign
from masonite.controllers import Controller
from masonite.request import Request

from config.auth import AUTH
from config.admin import LOGIN_CONF
from admin.web.LoginToken import LoginToken

# try:
#     from app.models.LoginToken import LoginToken
# except:
#     from app.LoginToken import LoginToken


class LoginController(Controller):
    def store(self, request: Request):
        email = request.input('email')
        password = request.input('password')
        user = AUTH['model'].where('email', email).first()
        login = checkpw(bytes(password, 'utf-8'), bytes(user.password, 'utf-8'))
        if login:
            hash = LoginToken().login(int(user.id))
            return {'login': True, 'token': hash, 'id': user.id, 'name': user.name}


            # Delete existing token
            # LoginToken.where('admin_user_id', user.id).delete()
            # hash = secrets.token_urlsafe()

            # login_token = LoginToken()
            # login_token.admin_user_id = user.id
            # login_token.token = hash
            # login_token.save()
            # return {'login': True, 'token': hash, 'id': user.id, 'name': user.name}
        else:
            return {'login': False}

    def destroy(self, request: Request):
        login_id = request.input('login_id')
        # LoginToken.where('admin_user_id', login_id).delete()
        LoginToken().logout(int(login_id))
        return {}
