""" A AdminProvider Service Provider """

import os
from masonite.provider import ServiceProvider
from .commands.TestCommand import Test
from .commands.CreateSuperUserCommand import CreateSuperUser

package_directory = os.path.dirname(os.path.realpath(__file__))

class AdminProvider(ServiceProvider):
    """Provides Services To The Service Container
    """

    wsgi = False

    def register(self):
        """Register objects into the Service Container
        """
        self.app.bind('AdminCommand', Test())
        self.app.bind('CreateSuperUserCommand', CreateSuperUser())
        self.app.bind(
            'AdminUserMigrationDirectory',
            os.path.join(package_directory, 'migrations')
        )

    def boot(self):
        """Boots services required by the container
        """

        pass