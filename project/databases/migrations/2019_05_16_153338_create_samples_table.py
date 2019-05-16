from orator.migrations import Migration


class CreateSamplesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('samples') as table:
            table.increments('id')
            table.big_increments('big_increments')
            table.big_integer('big_integer')
            table.binary('binary')
            table.boolean('boolean')
            table.char('char', 4)
            table.date('date')
            table.datetime('datetime')
            table.decimal('decimal', 5, 2)
            table.double('double', 15, 8)
            table.enum('enum', ['foo', 'bar'])
            table.float('float')
            table.integer('integer')
            table.json('json')
            table.long_text('long_text')
            table.medium_integer('medium_integer')
            table.medium_text('medium_text')
            table.morphs('morphs')
            table.small_integer('small_integer')
            table.string('string')
            table.string('string_with_len', 100)
            table.text('text')
            table.time('time')
            table.timestamp('timestamp')
            table.soft_deletes()
            table.timestamps()
            table.integer('user_id').unsigned()
            table.foreign('user_id').references('id').on('users').on_delete('cascade')
            table.integer('post_id').unsigned()
            table.foreign('post_id').references('id').on('posts').on_delete('cascade')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('samples')
