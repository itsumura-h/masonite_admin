"""TestSchema Testcase."""

from masonite.testing import TestCase
from admin.web.schema.SchemaService import SchemaService
from app.User import User
from config.admin import MODELS


class TestSchema(TestCase):

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

    def test_foreign_data(self):
        result = SchemaService._foreign_data(SchemaService, 'users')
        foreign_data = User.select('id', 'name as data').get().serialize()
        assert result == foreign_data

    def test_model_row_by_table_name(self):
        result = SchemaService.get_model_row_by_table_name('users')
        assert result == MODELS[0]