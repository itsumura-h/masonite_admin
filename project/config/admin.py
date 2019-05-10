from app.User import User
from app.models.Post import Post

MODELS = [
    {
        'model': User,
        'create_display': ['name', 'email', 'password'],
        'list_display': ['name', 'email'],
        'detail_display': ['name', 'email', 'password'],
        'foreign_display': 'name',
        'hash': ['password']
    },
    {
        'model': Post,
        'create_display': ['title', 'posts', 'user_id'],
        'list_display': ['title', 'posts'],
        'detail_display': ['title', 'posts', 'user_id']
    }
]

CONFIG = {
    'DB': 'pickle', # 'sqlite', 'mysql', 'pgsql'
}


# import pprint, inspect
# pprint.pprint(inspect.getmembers(User))
# print(User.__doc__.split(' ')[0])
# print(Post.__doc__.split(' ')[0])
# pprint.pprint(Post.__table__)