"""Testlogout Testcase."""

from masonite.testing import TestCase
from app.models.AdminUser import AdminUser
from masonite.helpers import password as bcrypt_password
import json
from pprint import pprint


class TestLogout(TestCase):

    """All tests by default will run inside of a database transaction."""
    transactions = True

    def setUp(self):
        """Anytime you override the setUp method you must call the setUp method
        on the parent class like below.
        """
        super().setUp()

    def setUpFactories(self):
        """This runs when the test class first starts up.
        This does not run before every test case. Use this method to
        set your database up.
        """
        # create_new_admin_user
        AdminUser.insert({
            'name': 'test_admin',
            'email': 'test_admin@test.com',
            'password': bcrypt_password('TestPassword1'),
            'permission': '1'
        })

    def test_logout_invalid_id(self):
        response = json.loads(
            self.post('/admin/api/login', {
                'email': 'test_admin@test.com',
                'password': 'TestPassword1'
            })
            .container
            .providers['Response']
        )

        token = response['token']

        self.assertFalse(
            self.post('/admin/api/logout', {
                'login_id': 1,
                'login_token': token
            })
            .ok()
        )

    def test_logout_invalid_token(self):
        response = json.loads(
            self.post('/admin/api/login', {
                'email': 'test_admin@test.com',
                'password': 'TestPassword1'
            })
            .container
            .providers['Response']
        )

        id = response['id']

        self.assertFalse(
            self.post('/admin/api/logout', {
                'login_id': id,
                'login_token': 'aaa'
            })
            .ok()
        )

    def test_logout_ok(self):
        response = json.loads(
            self.post('/admin/api/login', {
                'email': 'test_admin@test.com',
                'password': 'TestPassword1'
            })
            .container
            .providers['Response']
        )

        id = response['id']
        token = response['token']

        self.assertTrue(
            self.post('/admin/api/logout', {
                'login_id': id,
                'login_token': token
            })
            .ok()
        )
