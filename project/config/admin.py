from app.User import User
from app.models.Post import Post

CONFIG = [
    {
        'model': User,
        'table': 'users',
        'list_display': ['name', 'email']
    },
    {
        'model': Post,
        'table': 'posts',
        'list_display': ['title', 'posts']
    }
]
