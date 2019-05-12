from app.User import User
from app.models.Post import Post
#from app.models.AdminUser import AdminUser

MODELS = [
    # {
    #     'model':AdminUser,
    #     'list_display': ['name', 'email'],
    #     'detail_display': ['name', 'email'],
    # },
    {
        'model': User,
        'create_display': ['name', 'email', 'password'],
        'list_display': ['name', 'email'],
        'detail_display': ['name', 'email', 'password'],
        'foreign_display': 'name',
    },
    {
        'model': Post,
        'create_display': ['title', 'posts', 'user_id'],
        'list_display': ['title', 'posts'],
        'detail_display': ['title', 'posts', 'user_id']
    }
]
