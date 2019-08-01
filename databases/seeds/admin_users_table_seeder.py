from pprint import pprint

from faker import Faker
from masonite.helpers import password as bcrypt_password
from orator.orm import Factory
from orator.seeds import Seeder

from app.models.AdminUser import AdminUser


class AdminUserTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        admin_users = [
            {
                'name': f'user{str(i)}',
                'email': f'user{str(i)}@gmail.com',
                'password': bcrypt_password(f'Password{str(i)}'),
                # even→2(staff), odd→3(user)
                'permission': 2 if i % 2 == 0 else 3
            } for i in range(1, 100)
        ]
        AdminUser.insert(admin_users)

    def admin_users_factory(self, faker):
        return {
            'name': 'admin',
            'email': 'admin@test.com',
            'password': bcrypt_password('admin')
        }
