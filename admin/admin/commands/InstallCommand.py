""" A CreateSuperUser Command """
from cleo import Command
import os
from subprocess import check_output

# add routes
from masonite.packages import append_web_routes

class Install(Command):
    """
    Install admin package: create model and config

    admin:install
    """
    def handle(self):
        #==================== Create config ====================
        filedata = '''"""
admin conf

Exmaple
===================================================

from app.User import User
from app.models.Post import Post
MODELS = [
    {
        'model': User,
        'model_str': 'ユーザー一覧',
        'create_display': ['name', 'email'],
        'list_display': ['name', 'email'],
        'detail_display': ['name', 'email'],
        'foreign_display': 'name',
    },
    {
        'model': Post,
        'create_display': ['title', 'posts', 'user_id'],
        'list_display': ['title', 'posts'],
        'detail_display': ['title', 'posts', 'user_id']
    }
]

===================================================

model (ModelClass): required
    set model class. This item is always necessary.

model_str (str): optional
    Displaying name in drawer. It is useful for users who are not English speaker.

create_display (list[str]): optional
    Lists of columns you want to display in create page.

list_display (list[str]): optional
    Lists of columns you want to display in index page.

detail_display (list[str]): optional
    Lists of columns you want to display in show and edit pages.

foreign_display (str): optional
    When this model is called through foreign key, this column's data will be displayed as a string.

---
If optional setting is not set, all columns will be displayed.
If foreign_display is not set, primary key will be displayed as a number.

_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_

LOGIN_CONF Exmaple
===================================================

from datetime import timedelta
LOGIN_CONF = {
    'file_path': 'databases/login.bin',
    'timeout': timedelta(hours=1)
}

===================================================

file_path (str): optional
    Define where Login Token Pickle file is.
    if not set, system use 'databases/login.bin' by default.

timeout (timedelta): optional
    Define how much time server is not access
    if not set, system use '1 hour' by default.

"""

MODELS = []

from datetime import timedelta
LOGIN_CONF = {
    'file_path': 'databases/login.bin',
    'timeout': timedelta(hours=1),
}
'''

        config_path = 'config/admin.py'
        is_config_exists = os.path.exists(config_path)
        if not is_config_exists:
            with open(config_path, 'w') as f:
                f.write(filedata)
            self.line('<info>'+config_path+' Created Successfully!</info>')
        else:
            self.line('<info>'+config_path+' Already Exists!</info>')

        #==================== Create model ====================
        #whether models dir is exists
        isdir = os.path.isdir('app/models')

        if(isdir):
            admin_user_model_path = 'app/models/AdminUser.py'
            admin_user_output = bytes(check_output(
                    ['craft', 'model', 'models/AdminUser']
                )).decode('utf-8')
            admin_user_output = ''.join(admin_user_output.splitlines()) # to delete new line

            # login_token_model_path = 'app/models/LoginToken.py'
            # login_token_output = bytes(check_output(
            #         ['craft', 'model', 'models/LoginToken']
            #     )).decode('utf-8')
            # login_token_output = ''.join(login_token_output.splitlines()) # to delete new line
        else:
            admin_user_model_path = 'app/AdminUser.py'
            admin_user_output = bytes(check_output(
                    ['craft', 'model', 'AdminUser']
                )).decode('utf-8')

            # login_token_model_path = 'app/LoginToken.py'
            # login_token_output = bytes(check_output(
            #         ['craft', 'model', 'LoginToken']
            #     )).decode('utf-8')

        self.line('<info>AdminUser '+admin_user_output+'</info>')
        # self.line('<info>LoginToken '+login_token_output+'</info>')

        #==================== Edit Middleware ====================
        filedata = '''
from masonite.request import Request
from masonite.response import Response

# from app.models.LoginToken import LoginToken
from admin.web.LoginToken import LoginToken
from config.admin import LOGIN_CONF

import pickle, datetime

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
        pass

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

'''
        middleware_path = 'app/http/middleware/AdminMiddleware.py'
        with open(middleware_path, 'w') as f:
            f.write(filedata)

        # with open(middleware_path, 'r') as f:
        #     filedata = f.read()

        # if "#LoginToken" in filedata:
        #     if isdir:
        #         filedata = filedata.replace('#LoginToken', 'from app.models.LoginToken import LoginToken')
        #     else:
        #         filedata = filedata.replace('#LoginToken', 'from app.LoginToken import LoginToken')

        #     with open(middleware_path, 'w') as f:
        #         f.write(filedata)

        #     self.line('<info>Edit '+middleware_path+' Successfully!</info>')
        # else:
        #     self.line('<info>'+middleware_path+' Is Already Edited!</info>')

        #==================== Edit Middleware Config ====================
        middleware_conf_path = 'config/middleware.py'
        with open(middleware_conf_path, 'r') as f:
            filedata = f.read()

        if "ROUTE_MIDDLEWARE['admin'] = AdminMiddleware" in filedata or \
        "'admin': AdminMiddleware" in filedata:
            self.line('<info>'+middleware_conf_path+' Is Already Edited!</info>')
        else:
            lines = [
                "",
                "from app.http.middleware.AdminMiddleware import AdminMiddleware",
                "ROUTE_MIDDLEWARE['admin'] = AdminMiddleware"
                ""
            ]
            with open(middleware_conf_path, 'a') as f:
                f.write('\n'.join(lines))
            self.line('<info>Edit '+middleware_conf_path+' Successfully!</info>')

        #==================== Edit CSRF Middleware ====================
        csrf_middleware_path = 'app/http/middleware/CsrfMiddleware.py'

        with open(csrf_middleware_path, 'r') as f:
            filedata = f.read()

        if 'admin/*' in filedata:
            self.line('<info>'+csrf_middleware_path+' Is Already Edited!</info>')
        else:
            lines = [
                "",
                "    exempt += ['/admin/*']",
            ]
            with open(csrf_middleware_path, 'a') as f:
                f.write('\n'.join(lines))
            self.line('<info>Edit '+csrf_middleware_path+' Successfully!</info>')

        #==================== Edit Auth ====================
        auth_path = 'config/auth.py'
        with open(auth_path, 'r') as f:
            filedata = f.read()

        if "'model': User," in filedata:
            if isdir:
                filedata = filedata.replace("from app.User import User", "from app.models.AdminUser import AdminUser")
            else:
                filedata = filedata.replace("from app.User import User", "from app.AdminUser import AdminUser")

            filedata = filedata.replace("'model': User,", "'model': AdminUser,")

            with open(auth_path, 'w') as f:
                f.write(filedata)

            self.line('<info>Edit '+auth_path+' Successfully!</info>')
        else:
            self.line('<info>'+auth_path+' Is Already Edited!</info>')

        #==================== Add routes ====================
        content = None
        route_path = 'routes/web.py'
        with open(route_path, 'r') as f:
            content = f.read()
        if "ADMIN_ROUTES" in content:
            self.line('<info>Admin Routes Already Exists!</info>')
        else:
            lines = [
                "",
                "from admin.web.admin_routes import ADMIN_ROUTES, ADMIN_ROUTES_WITH_MIDDLEWARE, MODEL_ROUTES",
                "",
                "ROUTES += [",
                "    RouteGroup(ADMIN_ROUTES_WITH_MIDDLEWARE, prefix='/admin', middleware=('admin',)),",
                "    RouteGroup(MODEL_ROUTES, prefix='/admin', middleware=('admin_model',)), #middleware not working",
                "    RouteGroup(ADMIN_ROUTES, prefix='/admin'),",
                "]",
                ""
            ]
            with open(route_path, 'a') as f:
                f.write('\n'.join(lines))
            self.line('<info>Admin Routes Appended Successfully!</info>')

        #==================== Last message ====================
        self.line('<info>Install Compleated for...</info>')
        self.line('    <comment>'+config_path+'</comment>')
        self.line('    <comment>'+auth_path+'</comment>')
        self.line('    <comment>'+middleware_conf_path+'</comment>')
        self.line('    <comment>'+csrf_middleware_path+'</comment>')
        self.line('    <comment>'+admin_user_model_path+'</comment>')
        # self.line('    <comment>'+login_token_model_path+'</comment>')
        self.line('    <comment>'+route_path+'</comment>')
