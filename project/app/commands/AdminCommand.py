""" A AdminCommand Command """
from cleo import Command


class AdminCommand(Command):
    """
    Admin Command

    admin:set
        {argument : description}
    """

    def handle(self):
        argument = self.argument('argument')
        print('Masonite Admin '+argument)