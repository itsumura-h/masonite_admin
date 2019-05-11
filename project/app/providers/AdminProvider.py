""" A AdminProvider Service Provider """

from masonite.provider import ServiceProvider
from app.commands.AdminCommand import AdminCommand


class AdminProvider(ServiceProvider):
    """Provides Services To The Service Container
    """

    wsgi = False
    
    def register(self):
        """Register objects into the Service Container
        """
        self.app.bind('AdminCommand', AdminCommand())

    def boot(self):
        """Boots services required by the container
        """

        pass