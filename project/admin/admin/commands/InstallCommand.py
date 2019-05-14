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
        config_path = 'config/admin.py'
        is_config_exists = os.path.exists(config_path)
        if not is_config_exists:
            with open(config_path, 'w') as f:
                f.write('MODELS = []')
            self.line('<info>Config Created Successfully!</info>')
        else:
            self.line('<info>Config Already Exists!</info>')

        #==================== Create model ====================
        #whether models dir is exists
        isdir = os.path.isdir('app/models')

        if(isdir):
            admin_user_model_path = 'app/models/AdminUser.py'
            login_token_model_path = 'app/models/LoginToken.py'
            admin_user_output = bytes(check_output(
                    ['craft', 'model', 'models/AdminUser']
                )).decode('utf-8')
            login_token_output = bytes(check_output(
                    ['craft', 'model', 'models/LoginToken']
                )).decode('utf-8')
        else:
            admin_user_model_path = 'app/AdminUser.py'
            login_token_model_path = 'app/LoginToken.py'
            admin_user_output = bytes(check_output(
                    ['craft', 'model', 'AdminUser']
                )).decode('utf-8')
            login_token_output = bytes(check_output(
                    ['craft', 'model', 'LoginToken']
                )).decode('utf-8')

        self.line('<info>AdminUser '+admin_user_output+'</info>')
        self.line('<info>LoginToken '+login_token_output+'</info>')

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
            self.line('<info>'+auth_path+' Already Edited!</info>')

        #==================== Add routes ====================
        content = None
        route_path = 'routes/web.py'
        with open(route_path, 'r') as f:
            content = f.read()
        if "ADMIN_ROUTES" in content:
            self.line('<info>Admin Routes Already Exists!</info>')
        else:
            #append_web_routes('admin/admin/web/admin_routes.py')
            lines = [
                "",
                "from admin.web.admin_routes import ADMIN_ROUTES, ADMIN_ROUTES_WITH_MIDDLEWARE, MODEL_ROUTES",
                "",
                "ROUTES += [",
                "    RouteGroup(ADMIN_ROUTES_WITH_MIDDLEWARE, prefix='/admin', middleware=('admin',)),",
                "    RouteGroup(MODEL_ROUTES, prefix='/admin', middleware=('admin_model',)), #middleware not working",
                "    RouteGroup(ADMIN_ROUTES, prefix='/admin'),",
                "]"
            ]
            with open(route_path, 'a') as f:
                f.write('\n'.join(lines))
            self.line('<info>Admin Routes Appended Successfully!</info>')

        #==================== Last message ====================
        self.line('<info>Install Compleated for...</info>')
        self.line('    <comment>'+config_path+'</comment>')
        self.line('    <comment>'+auth_path+'</comment>')
        self.line('    <comment>'+admin_user_model_path+'</comment>')
        self.line('    <comment>'+login_token_model_path+'</comment>')
        self.line('    <comment>'+route_path+'</comment>')