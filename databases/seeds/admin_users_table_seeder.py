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
        admin_users = []
        for i in range(100):
            admin_users.append(
                {
                    'name': 'user'+str(i),
                    'email': 'test'+str(i)+'@gmail.com',
                    'password': bcrypt_password('Password'+str(i))
                }
            )
        AdminUser.insert(admin_users)

        # self.factory.register(AdminUser, self.admin_users_factory)
        # self.faker = Faker('en')
        # self.factory(AdminUser, 1).create()

    def admin_users_factory(self, faker):
        return {
            'name': 'admin',
            'email': 'admin@test.com',
            'password': bcrypt_password('admin')
        }
