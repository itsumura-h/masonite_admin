from orator.migrations import Migration


class CreateAdminUsersTable(Migration):

    def up(self):
        """Run the migrations."""
        with self.schema.create('admin_users') as table:
            table.increments('id')
            table.string('name')
            table.string('email').unique()
            table.string('password')
            table.timestamps()

    def down(self):
        """Revert the migrations."""
        self.schema.drop('admin_users')
