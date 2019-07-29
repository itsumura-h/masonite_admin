"""Administrator Middleware."""

from masonite.request import Request
from masonite.response import Response


class AdministratorMiddleware:
    """Administrator Middleware."""

    def __init__(self, request: Request, response: Response):
        """Inject Any Dependencies From The Service Container.

        Arguments:
            Request {masonite.request.Request} -- The Masonite request object
        """
        self.request = request
        self.response = response

    def before(self):
        """Run This Middleware Before The Route Executes."""
        self.check_administrator()

    def after(self):
        """Run This Middleware After The Route Executes."""
        pass

    def check_administrator(self):
        permission = self.request.input('login_permission')
        if permission != 'administrator':
            return self.response.json(None, status=403)