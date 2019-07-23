from orator.orm import Factory
from orator.seeds import Seeder
from faker import Faker
from masonite.helpers import password as bcrypt_password
from app.models.AdminUser import AdminUser
from pprint import pprint

class AdminUserTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        admin_users = [
            {
                'name': f'user{str(i)}',
                'email': f'test{str(i)}@gmail.com',
                'password': bcrypt_password(f'Password{str(i)}'),
                'permission': 2 if i % 2 == 0 else 3 #even→2(staff), odd→3(user)
            } for i in range(100)
        ]
        AdminUser.insert(admin_users)

    def admin_users_factory(self, faker):
        return {
            'name': 'admin',
            'email': 'admin@test.com',
            'password': bcrypt_password('admin')
        }
