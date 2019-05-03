from app.User import User
from app.models.Post import Post

CONFIG = [
    {
        'model': User,
        'list_display': ['name', 'email'],
        'foreign_display': 'name',
    },
    {
        'model': Post,
        'list_display': ['title', 'posts'],
        'detail_display': ['title', 'posts', 'user_id']
    }
]


# import pprint, inspect
# pprint.pprint(inspect.getmembers(User))
# print(User.__doc__.split(' ')[0])
# print(Post.__doc__.split(' ')[0])
# pprint.pprint(Post.__table__)