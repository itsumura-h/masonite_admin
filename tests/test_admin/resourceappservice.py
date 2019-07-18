"""TestResourceAppService Testcase."""

from masonite.testing import TestCase
from admin.web.Resource.ResourceAppService import ResourceAppService
from datetime import date, datetime, time, timedelta
from pprint import pprint

class TestResourceAppService(TestCase):

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
        pass

    def test_001_arr_iso_format(self):
        today = datetime.today()
        date_diff = today - datetime(2000, 1, 1)
        test_data = {
            'str': 'str_value',
            'int': 2,
            'date': today.date(),
            'datetime': today,
            'time': today.time(),
            'timedelda': date_diff,
            'dict': {
                'str': 'str_value',
                'int': 2,
                'date': today.date(),
                'datetime': today,
                'time': today.time(),
                'timedelda': date_diff,
                'dict': {
                    'str': 'str_value',
                    'int': 2,
                    'date': today.date(),
                    'datetime': today,
                    'time': today.time(),
                    'timedelda': date_diff,
                }
            }
        }

        result = ResourceAppService().arr_iso_format(test_data)
        assert isinstance(result['int'], int)
        assert isinstance(result['date'], str)
        assert isinstance(result['datetime'], str)
        assert isinstance(result['time'], str)
        assert isinstance(result['timedelda'], str)

        assert isinstance(result['dict']['int'], int)
        assert isinstance(result['dict']['date'], str)
        assert isinstance(result['dict']['datetime'], str)
        assert isinstance(result['dict']['time'], str)
        assert isinstance(result['dict']['timedelda'], str)

        assert isinstance(result['dict']['dict']['int'], int)
        assert isinstance(result['dict']['dict']['date'], str)
        assert isinstance(result['dict']['dict']['datetime'], str)
        assert isinstance(result['dict']['dict']['time'], str)
        assert isinstance(result['dict']['dict']['timedelda'], str)

    def test_002_delete_login_params(self):
        params = {
            'test1': 'aaa',
            'test2': 'bbb',
            'login_id': 3,
            'login_token': 'qwertyuiop',
            'permission': 2,
            '__token': 'qwertyuiop'
        }

        params = ResourceAppService.delete_login_params(params)
        pprint(params)
        assert params == {
            'test1': 'aaa',
            'test2': 'bbb',
        }
