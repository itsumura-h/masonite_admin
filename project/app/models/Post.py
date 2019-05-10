"""Post Model"""
"""Model Definition (generated with love by Masonite) 

id: integer default: None
title: string(255) default: None
posts: text default: None
created_at: datetime default: CURRENT_TIMESTAMP
updated_at: datetime default: CURRENT_TIMESTAMP
user_id: integer default: None
"""
from config.database import Model


class Post(Model):
    """Post Model"""
    #__table__ = 'posts'