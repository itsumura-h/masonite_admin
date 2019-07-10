from bcrypt import checkpw
from masonite.controllers import Controller
from masonite.request import Request

from admin.web.Login.LoginService import LoginService
from config.auth import AUTH


class LoginController(Controller):
    def store(self, request: Request):
        email = request.input('email')
        password = request.input('password')
        user = AUTH['model'].where('email', email).first()
        login = checkpw(bytes(password, 'utf-8'),
                        bytes(user.password, 'utf-8'))

        if login:
            hash = LoginService().login(int(user.id), int(user.permission))
            return {
                'login': True,
                'token': hash,
                'id': user.id,
                'name': user.name,
                'permission': user.permission
            }
        else:
            return {'login': False}

    def destroy(self, request: Request):
        login_id = request.input('login_id')
        LoginService().logout(int(login_id))
        return ''
