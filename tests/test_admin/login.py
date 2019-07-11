"""Testlogin Testcase."""

from masonite.testing import TestCase
from app.models.AdminUser import AdminUser
from masonite.helpers import password as bcrypt_password


class TestLogin(TestCase):

    """All tests by default will run inside of a database transaction."""
    transactions = True

    def setUp(self):
        """Anytime you override the setUp method you must call the setUp method
        on the parent class like below."""
        super().setUp()

    def setUpFactories(self):
        """This runs when the test class first starts up.

        This does not run before every test case. Use this method to set
        your database up.
        """
        # create_new_admin_user
        AdminUser.insert({
            'name': 'test_admin',
            'email': 'test_admin@test.com',
            'password': bcrypt_password('TestPassword1'),
            'permission': '1'
        })

    def test_login_ok(self):
        assert self.post('/admin/api/login', {
            'email': 'test_admin@test.com',
            'password': 'TestPassword1'
        }).ok()

    def test_login_response(self):
        access = self.json('POST', '/admin/api/login', {
            'email': 'test_admin@test.com',
            'password': 'TestPassword1'
        })

        assert access.hasJson('login', True)
        assert access.hasJson('name', 'test_admin')
        assert access.hasJson('permission', '1')

    def test_login_reeponse_str(self):
        access = self.post('/admin/api/login', {
            'email': 'test_admin@test.com',
            'password': 'TestPassword1'
        })

        assert access.contains('id')
        assert access.contains('token')

    def test_login_invalid_email(self):
        access = self.post('/admin/api/login', {
            'email': 'invalid@test.com',
            'password': 'invalid'
        })

        self.assertFalse(
            access.ok()
        )

    def test_login_invalid_password(self):
        access = self.post('/admin/api/login', {
            'email': 'test_admin@test.com',
            'password': 'invalid'
        })

        self.assertFalse(
            access.ok()
        )
