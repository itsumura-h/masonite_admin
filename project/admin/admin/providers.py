""" A AdminProvider Service Provider """

from masonite.provider import ServiceProvider
from .commands.TestCommand import Test
from .commands.CreateSuperUserCommand import CreateSuperUser


class AdminProvider(ServiceProvider):
    """Provides Services To The Service Container
    """

    wsgi = False
    
    def register(self):
        """Register objects into the Service Container
        """
        self.app.bind('AdminCommand', Test())
        self.app.bind('CreateSuperUserCommand', CreateSuperUser())

    def boot(self):
        """Boots services required by the container
        """

        pass