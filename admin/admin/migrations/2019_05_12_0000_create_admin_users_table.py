from orator.migrations import Migration


class CreateAdminUsersTable(Migration):

    def up(self):
        """Run the migrations."""
        with self.schema.create('admin_users') as table:
            table.increments('id')
            table.string('name')
            table.string('email').unique()
            table.string('password')
            table.enum('permission', [1, 2, 3])
            table.timestamps()

    def down(self):
        """Revert the migrations."""
        self.schema.drop('admin_users')


'''
from orator.migrations import Migration


class CreateLoginTokensTable(Migration):

    def up(self):
        """Run the migrations."""
        with self.schema.create('login_tokens') as table:
            table.increments('id')
            table.integer('admin_user_id').unsigned()
            table.foreign('admin_user_id').references('id').on('admin_users').on_delete('cascade')
            table.string('token')
            table.timestamps()

    def down(self):
        """Revert the migrations."""
        self.schema.drop('login_tokens')
'''