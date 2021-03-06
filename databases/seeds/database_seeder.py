"""Base Database Seeder Module."""

from orator.seeds import Seeder
from .user_table_seeder import UserTableSeeder
from .posts_table_seeder import PostsTableSeeder
from .admin_users_table_seeder import AdminUserTableSeeder

class DatabaseSeeder(Seeder):

    def run(self):
        """Run the database seeds."""
        self.call(UserTableSeeder)
        self.call(PostsTableSeeder)
        self.call(AdminUserTableSeeder)