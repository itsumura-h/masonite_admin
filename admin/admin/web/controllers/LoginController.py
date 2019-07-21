from bcrypt import checkpw
from masonite.controllers import Controller
from masonite.request import Request
from masonite.response import Response

from admin.web.Login.LoginService import LoginService


class LoginController(Controller):
    def store(self, request: Request, response: Response):
        email = request.input('email')
        password = request.input('password')
        try:
            user = LoginService().get_user(email)
            login = checkpw(bytes(password, 'utf-8'),
                            bytes(user.password, 'utf-8'))

            if login:
                hash = LoginService().login(int(user.id), user.permission)
                return {
                    'login': True,
                    'token': hash,
                    'id': user.id,
                    'name': user.name,
                    'permission': user.permission
                }
            else:
                raise Exception
        except Exception:
            return response.json({'login': False}, status=403)

    def destroy(self, request: Request, response: Response):
        login_id = request.input('login_id')
        login_token = request.input('login_token')
        is_logout_success = LoginService().logout(int(login_id), login_token)

        if is_logout_success:
            return ''
        else:
            return response.view('invalid user', status=403)