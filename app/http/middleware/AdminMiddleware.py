
import datetime, pickle

from masonite.request import Request
from masonite.response import Response

from admin.web.LoginToken import LoginToken
from config.admin import LOGIN_CONF

timeout = datetime.timedelta(hours=1)

class AdminMiddleware:
    """Check token
    """

    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response
        self.timeout = LOGIN_CONF['timeout'] if 'timeout' in LOGIN_CONF else timeout
        if not isinstance(self.timeout, datetime.timedelta):
            self.timeout = timeout

        self.login_token = LoginToken()

    def before(self):
        return self.checkpw()

    def after(self):
        # To hundle Pypy GC error. Request's instans is reused.
        self.request.request_variables = {}

    def checkpw(self):
        if self.checkpw_resource() == False:
            return self.response.json(None, status=403)

    def checkpw_resource(self):
        try:
            admin_user_id = self.request.input('login_id')
            input_token = self.request.input('login_token')

            # db_token = LoginToken.where('admin_user_id', admin_user_id).first().token
            login_data = self.login_token.load()[int(admin_user_id)]

            # check token is exists
            db_token = login_data['token']
            if db_token == None or input_token != db_token:
                return False

            # check whther admin is not edited
            permission = self.request.input('permission')
            if int(login_data['permission']) != int(permission):
                return False

            # check timeout
            diff = datetime.datetime.now() - login_data['last_access']
            if diff > self.timeout:
                self.login_token.logout(admin_user_id)
                return False
            else:
                self.login_token.update_last_access(int(admin_user_id))

            return True

        except Exception as e:
            return False

