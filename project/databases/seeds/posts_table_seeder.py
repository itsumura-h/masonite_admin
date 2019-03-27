from orator.orm import Factory
from orator.seeds import Seeder
from faker import Faker

from app.models.Post import Post

import random

class PostsTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.factory.register(Post, self.posts_factory)
        self.factory(Post, 100).create()

    def posts_factory(self):
        fake = Faker('ja')
        return {
            'title': fake.sentences(nb=1, ext_word_list=None)[0],
            'posts': fake.text(max_nb_chars=200, ext_word_list=None),
            'user_id': random.randint(0, 19)
        }