""" A CreateSuperUser Command """
from cleo import Command
import os
from subprocess import check_output

# add routes
from masonite.packages import append_web_routes

class Install(Command):
    """
    Install admin package, create model, seed, config

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
            model_path = 'app/models/AdminUser.py'
            output = bytes(check_output(
                    ['craft', 'model', 'models/AdminUser']
                )).decode('utf-8')
        else:
            model_path = 'app/AdminUser.py'
            output = bytes(check_output(
                    ['craft', 'model', 'AdminUser']
                )).decode('utf-8')

        self.line('<info>'+output+'</info>')

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

        #==================== Create seeder ====================
        if isdir:
            seeder = '''from orator.orm import Factory
from orator.seeds import Seeder
from faker import Faker
from masonite.helpers import password as bcrypt_password
from app.models.AdminUser import AdminUser

class AdminUserTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.factory.register(AdminUser, self.admin_users_factory)
        self.faker = Faker('en')
        self.factory(AdminUser, 1).create()

    def admin_users_factory(self, faker):
        return {
            'name': 'admin',
            'email': 'admin@test.com',
            'password': bcrypt_password('admin')
        }
'''
        else:
            seeder = '''from orator.orm import Factory
from orator.seeds import Seeder
from faker import Faker
from masonite.helpers import password as bcrypt_password
from app.AdminUser import AdminUser

class AdminUserTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.factory.register(AdminUser, self.admin_users_factory)
        self.faker = Faker('en')
        self.factory(AdminUser, 1).create()

    def admin_users_factory(self, faker):
        return {
            'name': 'admin',
            'email': 'admin@test.com',
            'password': bcrypt_password('admin')
        }
'''

        seed_path = 'databases/seeds/admin_users_table_seeder.py'
        if(os.path.exists(seed_path)):
            self.line('<info>Seeder Already Exists!</info>')
        else:
            with open(seed_path, 'w') as f:
                f.write(seeder)
            self.line('<info>Seeder Created Successfully!</info>')

        #==================== Add routes ====================
        content = None
        route_path = 'routes/web.py'
        with open(route_path, 'r') as f:
            content = f.read()
        if "Admin Routes" in content:
            self.line('<info>Admin Routes Already Exists!</info>')
        else:
            append_web_routes('admin/admin/web/admin_routes.py')
            self.line('<info>Admin Routes Appended Successfully!</info>')

        #==================== Last message ====================
        self.line('<info>Install Compleated for...</info>')
        self.line('    <comment>'+config_path+'</comment>')
        self.line('    <comment>'+auth_path+'</comment>')
        self.line('    <comment>'+model_path+'</comment>')
        self.line('    <comment>'+seed_path+'</comment>')
        self.line('    <comment>'+route_path+'</comment>')