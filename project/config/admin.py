from app.User import User
from app.models.Post import Post

CONFIG = [
    {
        'model': User,
        'create_display': ['name', 'email', 'password'],
        'list_display': ['name', 'email'],
        'detail_display': ['name', 'email', 'updated_at'],
        'foreign_display': 'name',
    },
    {
        'model': Post,
        'create_display': ['title', 'posts', 'user_id'],
        'list_display': ['title', 'posts'],
        'detail_display': ['title', 'posts', 'user_id']
    }
]


# import pprint, inspect
# pprint.pprint(inspect.getmembers(User))
# print(User.__doc__.split(' ')[0])
# print(Post.__doc__.split(' ')[0])
# pprint.pprint(Post.__table__)