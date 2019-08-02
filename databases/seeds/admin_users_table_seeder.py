from pprint import pprint

from faker import Faker
from masonite.helpers import password as make_password
from orator.orm import Factory
from orator.seeds import Seeder
from datetime import date

from app.models.AdminUser import AdminUser


class AdminUserTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        users = [
            {
                'name': f'user{str(i)}',
                'email': f'user{str(i)}@gmail.com',
                'password': make_password(f'Password{str(i)}'),
                # even→2(staff), odd→3(user)
                'permission': 2 if i % 2 == 0 else 3
            } for i in range(1, 100)
        ]
        AdminUser.insert(users)

        users = [
            {
                'name': 'test_admin',
                'email': 'test_admin@gmail.com',
                'password': make_password(
                    f'test_admin_Password{date.today().year}'
                ),
                'permission': 1
            },
            {
                'name': 'test_member',
                'email': 'test_member@gmail.com',
                'password': make_password(
                    f'test_member_Password{date.today().year}'
                ),
                'permission': 2
            },
            {
                'name': 'test_user',
                'email': 'test_user@gmail.com',
                'password': make_password(
                    f'test_user_Password{date.today().year}'
                ),
                'permission': 3
            },
        ]
        AdminUser.insert(users)