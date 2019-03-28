"""User Table Seeder.

You can run this seeder in order to generate users. 

    - Each time it is ran it will generate 50 random users.
    - All users have the password of 'secret'.
    - You can run the seeder by running: craft seed:run.
"""

from orator.orm import Factory
from orator.seeds import Seeder
from faker import Faker
from masonite.helpers import password as bcrypt_password

from app.User import User

class UserTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.factory.register(User, self.users_factory)
        self.faker = Faker('en')
        self.factory(User, 50).create()

    def users_factory(self, faker):
        name = self.faker.name()
        return {
            'name': name,
            'email': self.faker.email(),
            #'password': '$2b$12$WMgb5Re1NqUr.uSRfQmPQeeGWudk/8/aNbVMpD1dR.Et83vfL8WAu',  # == 'secret'
            'password': bcrypt_password(name) # == name
        }
