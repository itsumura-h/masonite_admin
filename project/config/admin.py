from app.User import User
from app.models.Post import Post

CONFIG = [
    {
        'model': User,
        'table': 'user'
    },
    {
        'model': Post,
        'table': 'posts'
    }
]
