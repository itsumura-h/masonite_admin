from bcrypt import checkpw
from masonite.controllers import Controller
from masonite.request import Request
from masonite.response import Response

from ..domain.services.domain_services.LoginService import LoginService


class LoginController(Controller):
    def store(self, request: Request, response: Response):
        email = request.input('email')
        password = request.input('password')
        try:
            hash, user = LoginService().store(email, password)
            return {
                'login': True,
                'token': hash,
                'id': user['id'],
                'name': user['name'],
                'permission': user['permission']
            }
        except Exception as e:
            print(str(e))
            return response.json({'login': False}, status=403)

    def destroy(self, request: Request, response: Response):
        login_id = request.input('login_id')
        login_token = request.input('login_token')
        is_logout_success = LoginService().logout(int(login_id), login_token)

        if is_logout_success:
            return ''
        else:
            return response.view('invalid user', status=403)
