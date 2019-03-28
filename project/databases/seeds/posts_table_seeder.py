from orator.orm import Factory
from orator.seeds import Seeder
from faker import Faker

from app.models.Post import Post
from app.User import User

import random

class PostsTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.factory.register(Post, self.posts_factory)
        self.faker = Faker('en')
        self.factory(Post, 100).create()

    def posts_factory(self, faker):
        user_id = random.randint(1, 20)
        return {
            'title':  User.find(user_id).name + '---' + self.faker.sentences(nb=1, ext_word_list=None)[0],
            'posts': self.faker.text(max_nb_chars=200, ext_word_list=None),
            'user_id': user_id
        }