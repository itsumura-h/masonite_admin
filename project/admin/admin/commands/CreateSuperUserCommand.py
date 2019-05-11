""" A AdminCommand Command """
from cleo import Command


class CreateSuperUser(Command):
    """
    Create Super User

    admin:createsuperuser
    """
    def handle(self):
        print('super user')