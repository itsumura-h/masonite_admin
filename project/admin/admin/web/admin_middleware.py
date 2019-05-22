from masonite.request import Request
from masonite.response import Response
from app.models.LoginToken import LoginToken

class AdminMiddleware:
    """Check token
    """

    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response

    def before(self):
        return self.checkpw()

    def after(self):
        pass

    def checkpw(self):
        try:
            admin_user_id = self.request.input('login_id')
            input_token = self.request.input('login_token')

            db_token = LoginToken.where('admin_user_id', admin_user_id).first().token
            if db_token == None or input_token != db_token:
                return self.response.json(None, status=403)
        except:
            return self.response.json(None, status=403)

    def checkpw_resource(self):
        try:
            admin_user_id = self.request.input('login_id')
            input_token = self.request.input('login_token')

            db_token = LoginToken.where('admin_user_id', admin_user_id).first().token
            if db_token == None or input_token != db_token:
                return False
        except:
            return False