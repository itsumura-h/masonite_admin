"""TestInfo Testcase."""

from masonite.testing import TestCase
import inspect
from pprint import pprint
import requests
import json


class TestInfo(TestCase):
    """All tests by default will run inside of a database transaction."""
    transactions = True

    def setUp(self):
        """Anytime you override the setUp method you must call the setUp method
        on the parent class like below."""
        super().setUp()

        response = json.loads(
            self.post('/admin/api/login',
                {'email': 'test2@gmail.com', 'password': 'Password2'}
            )
            .container.providers['Response']
        )

        self.params = {
            'login_id': response['id'],
            'login_token': response['token'],
            'permission': response['permission']
        }

    def setUpFactories(self):
        """This runs when the test class first starts up.

        This does not run before every test case. Use this method to set
        your database up.
        """
        pass

    def test_route_exists(self):
        self.assertTrue(self.get('/admin/api/info'))

    def test_route_has_route_middleware(self):
        assert self.get('/admin/api/info').hasMiddleware('admin')

    def test_status_200(self):
        assert self.get('/admin/api/info', self.params).ok()

    def test_api_is_protected(self):
        self.assertFalse(self.get('/admin/api/info').ok())
