from app.User import User
from app.models.Post import Post

CONFIG = [
    {
        'model': User,
        'table': 'users'
    },
    {
        'model': Post,
        'table': 'posts'
    }
]
