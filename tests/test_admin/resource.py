"""TestResource Testcase."""

from masonite.testing import TestCase
from app.models.AdminUser import AdminUser
from app.User import User
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


    def test_001_schema(self):
        params = self.get_params()
        assert  self.get('/admin/api/schema/User', params).ok()

    def test_002_schema_create(self):
        params = self.get_params()
        assert  self.get('/admin/api/schema/create/User', params).ok()

    def test_003_schema_detail(self):
        params = self.get_params()
        assert  self.get('/admin/api/schema/detail/User', params).ok()

    def test_004_resource(self):
        # index
        params = self.get_params()
        assert self.get('/admin/api/User', params).ok()

        # count
        access = self.get('/admin/api/User/count', params)
        assert access.ok()
        assert access.contains('count')

        # create
        params['name'] = 'new_test_user'
        params['email'] = 'new_test@test.com'
        params['password'] = 'password'

        access = self.json('POST', '/admin/api/User', params)
        assert access.ok()

        response = json.loads(access.container.providers['Response'])
        user = User.select('id', 'name', 'email').find(response['id']).serialize()
        assert {'id' : response['id'], 'name': response['name'], 'email':response['email']} == user

        # show
        del params['name'], params['email'], params['password']
        self.assertTrue(self.json('GET', f'/admin/api/User/{response["id"]}', params) \
            .hasJson({
                'name': 'new_test_user',
                'email': 'new_test@test.com'
            })
        )

        # edit
        params['name'] = 'edited_name'
        access = self.json('POST', f'/admin/api/User/{response["id"]}/put', params)
        assert access.ok()

        del params['name']
        self.assertTrue(
            self.json('GET', f'/admin/api/User/{response["id"]}', params) \
                .hasJson({
                    'name': 'edited_name',
                })
        )

        # destroy
        access = self.json('POST', f'/admin/api/User/{response["id"]}/delete', params)
        assert access.ok()

        # data should not exist
        self.assertFalse(
            self.json('GET', f'/admin/api/User/{response["id"]}', params).ok()
        )

    def test_005_invalid_token_index_create(self):
        params = self.get_params()
        params['login_token'] = 'aaaaa'

        # index
        self.assertFalse(self.get('/admin/api/User', params).ok())

        params['name'] = 'new_test_user'
        params['email'] = 'new_test@test.com'
        params['password'] = 'password'

        # create
        access = self.json('POST', '/admin/api/User', params)
        self.assertFalse(access.ok())

    def test_006_invalid_token_show_edit_delete(self):
        # set test data
        params = self.get_params()
        params['name'] = 'new_test_user'
        params['email'] = 'new_test@test.com'
        params['password'] = 'password'

        access = self.json('POST', '/admin/api/User', params)
        response = json.loads(access.container.providers['Response'])

        # set invalid token
        params['login_token'] = 'aaaaa'

        # show
        del params['name'], params['email'], params['password']
        self.assertFalse(
            self.json('GET', f'/admin/api/User/{response["id"]}', params).ok()
        )

        # edit
        params['name'] = 'edited_name'
        access = self.json('POST', f'/admin/api/User/{response["id"]}/put', params)
        self.assertFalse(access.ok())

        del params['name']
        access = self.json('GET', f'/admin/api/User/{response["id"]}', params)
        self.assertFalse(access.ok())

        # destroy
        access = self.json('POST', f'/admin/api/User/{response["id"]}/delete', params)
        self.assertFalse(access.ok())
