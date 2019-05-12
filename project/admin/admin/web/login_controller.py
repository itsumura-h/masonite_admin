from masonite.controllers import Controller
from masonite.request import Request
from config.auth import AUTH
from bcrypt import checkpw

class LoginController(Controller):
    def store(self, request: Request):
        email = request.input('email')
        password = request.input('password')
        print(email)
        print(password)
        user = AUTH['model'].where('email', email).first()
        login = checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
        if login:
            return {'login': True}
        else:
            return {'login': False}

    def destroy(self, request: Request):
        pass