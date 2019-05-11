""" A AdminCommand Command """
from cleo import Command


class Test(Command):
    """
    Admin Command

    admin:test
        {argument : description}
    """

    def handle(self):
        argument = self.argument('argument')
        print('Masonite Admin '+argument)