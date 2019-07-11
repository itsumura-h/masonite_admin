"""Testroot Testcase."""

from masonite.testing import TestCase


class TestRoot(TestCase):

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

    def test_root_access(self):
        assert self.get('/admin').ok()
        assert self.get('/admin/login').ok()
        assert self.get('/admin/User').ok()
        assert self.get('/admin/create').ok()
        assert self.get('/admin/1').ok()
        assert self.get('/admin/User/1/edit').ok()
