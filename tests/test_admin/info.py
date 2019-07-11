"""TestInfo Testcase."""

from masonite.testing import TestCase


class TestInfo(TestCase):
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

    def test_route_exists(self):
        self.assertTrue(self.get('/admin/api/info'))

    def test_route_has_route_middleware(self):
        assert self.get('/admin/api/info').hasMiddleware('admin')

    def test_has_amount(self):
        print(vars(self.json('GET', '/admin/api/info').container))
        self.assertTrue(
            self.json('GET', '/admin/api/info').hasAmount('env', 7)
        )
