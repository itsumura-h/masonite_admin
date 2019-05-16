""" A CreateSuperUser Command """
from cleo import Command
from masonite.helpers import password as bcrypt_password
import os
import re
from config.auth import AUTH

class CreateSuperUser(Command):
    """
    Create admin account

    admin:createsuperuser
    """
    def handle(self):

        name = None
        default_name = 'Anonymous' if os.environ.get("USER") == None else os.environ.get("USER")
        while name == None:
            name = input('Username (leave blank to use '+ default_name +'):')
            if name == '':
                name = default_name
        self.line('<comment>'+name+'</comment>')

        email = None
        while email == None:
            email = input('Email address:')
            EMAIL_REGEX = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")

            if not EMAIL_REGEX.match(email):
                self.line('<error>Error: Enter a valid email address.</error>')
                email = None
        self.line('<comment>'+email+'</comment>')

        password = None
        password_check = None
        while password == None:
            password = input('Password:')

            #minimu length
            if len(password) < 8:
                self.line('<error>This password is too short. It must contain at least 8 character.</error>')
                password = None
            elif re.search('[a-z]',password) is None:
                self.line('<error>Make sure your password has a lower case letter in it.</error>')
                password = None
            elif re.search('[0-9]',password) is None:
                self.line('<error>Make sure your password has a number in it.</error>')
                password = None
            elif re.search('[A-Z]',password) is None:
                self.line('<error>Make sure your password has a capital letter in it.</error>')
                password = None

            if password:
                password_check = input('Password (again):')
                if password != password_check:
                    self.line("<error>Error: Your passwords didn't match.</error>")
                    password = None

        password = bcrypt_password(password)
        new_user = {'name': name, 'email': email, 'password': password}

        AUTH['model'].insert(new_user)

        self.line('<info>Superuser created successfully.</info>')
