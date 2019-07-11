"""TestResource Testcase."""

from masonite.testing import TestCase
from app.models.AdminUser import AdminUser
from masonite.helpers import password as bcrypt_password
from pprint import pprint
import json


class TestResource(TestCase):

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

    def get_params(self):
        response = json.loads(
            self.post('/admin/api/login',
                {'email': 'test_admin@test.com', 'password': 'TestPassword1'}
            )
            .container.providers['Response']
        )

        params = {
            'login_id': response['id'],
            'login_token': response['token'],
            'permission': response['permission']
        }
        return params

    def test_schema(self):
        params = self.get_params()
        assert  self.get('/admin/api/schema/User', params).ok()

    def test_schema_create(self):
        params = self.get_params()
        assert  self.get('/admin/api/schema/create/User', params).ok()

    def test_schema_detail(self):
        params = self.get_params()
        assert  self.get('/admin/api/schema/detail/User', params).ok()