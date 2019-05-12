from orator.orm import Factory
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
