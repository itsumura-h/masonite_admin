from masonite.request import Request
from masonite.response import Response

from ..domain.services.domain_services.ManageAuthService import \
    ManageAuthService


class MypageController:
    def show(self, request: Request, response: Response):
        try:
            id = request.input('login_id')
            user = ManageAuthService.show(id)
            return user
        except Exception as e:
            print(str(e))
            return response.json({'error': str(e)}, status=400)

    def update(self, request: Request, response: Response):
        try:
            id = request.input('login_id')
            params = request.all()
            is_success, new_user = ManageAuthService.update(id, params)
            if is_success:
                return {'new_user': new_user}
        except Exception as e:
            print(str(e))
            return response.json({'error': str(e)}, status=400)

    def reset_password(self, request: Request, response: Response):
        try:
            id = request.input('login_id')
            new_password = ManageAuthService.reset_password(id)
            return {'new_password': new_password}
        except Exception as e:
            return response.json({'error': str(e)}, status=400)

    def update_password(self, request: Request, response: Response):
        try:
            id = request.input('login_id')
            password = request.input('password')
            new_password = request.input('new_password')
            ManageAuthService.update_password(
                id,
                password,
                new_password
            )
            return ''
        except Exception as e:
            print(str(e))
            return response.json({'error': str(e)}, status=400)
