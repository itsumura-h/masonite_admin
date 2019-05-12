from orator.migrations import Migration


class CreateTokensTable(Migration):

    def up(self):
        """Run the migrations."""
        with self.schema.create('tokens') as table:
            table.big_increments('id')
            table.integer('admin_user_id').unsigned()
            table.foreign('admin_user_id').references('id').on('admin_users').on_delete('cascade')
            table.string('token', 40)
            table.datetime('access_at')

    def down(self):
        """Revert the migrations."""
        self.schema.drop('admin_users')
