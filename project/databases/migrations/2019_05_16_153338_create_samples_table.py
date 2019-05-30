from orator.migrations import Migration


class CreateSamplesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('samples') as table:
            """
            table.increments('id')
            table.date('date').nullable()
            table.datetime('datetime').nullable()
            table.time('time').nullable()
            table.timestamp('timestamp').nullable()
            table.timestamps()
            table.integer('user_id').unsigned().nullable()
            table.foreign('user_id').references('id').on('users').on_delete('cascade')
            table.integer('post_id').unsigned().nullable()
            table.foreign('post_id').references('id').on('posts').on_delete('cascade')
            """
            table.increments('id')
            table.big_integer('big_integer').nullable().default(1)
            table.binary('binary').nullable()
            table.boolean('boolean').nullable().default(0)
            table.char('char', 4).nullable()
            table.date('date').nullable()
            table.datetime('datetime').nullable()
            table.decimal('decimal', 5, 2).nullable()
            table.double('double', 15, 8).nullable()
            table.enum('enum', ['foo', 'bar'])
            table.float('float').nullable()
            table.integer('integer').nullable()
            table.json('json').nullable()
            table.long_text('long_text').nullable()
            table.medium_integer('medium_integer').nullable()
            table.medium_text('medium_text').nullable()
            table.morphs('morphs')
            table.small_integer('small_integer').nullable()
            table.string('string').nullable()
            table.string('string_with_len', 100).nullable()
            table.text('text').nullable()
            table.time('time').nullable()
            table.timestamp('timestamp').nullable()
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

"""

table.big_integer('big_integer').nullable().default(1)
table.binary('binary').nullable()
table.boolean('boolean').nullable().default(0)
table.char('char', 4).nullable()
table.date('date').nullable()
table.datetime('datetime').nullable()
table.decimal('decimal', 5, 2).nullable()
table.double('double', 15, 8).nullable()
table.enum('enum', ['foo', 'bar'])
table.float('float').nullable()
table.integer('integer').nullable()
table.json('json').nullable()
table.long_text('long_text').nullable()
table.medium_integer('medium_integer').nullable()
table.medium_text('medium_text').nullable()
#table.morphs('morphs')
table.small_integer('small_integer').nullable()
table.string('string').nullable()
table.string('string_with_len', 100).nullable()
table.text('text').nullable()
table.time('time').nullable()
table.timestamp('timestamp').nullable()
table.soft_deletes()
table.timestamps()
table.integer('user_id').unsigned()
table.foreign('user_id').references('id').on('users').on_delete('cascade')
table.integer('post_id').unsigned()
table.foreign('post_id').references('id').on('posts').on_delete('cascade')


"""