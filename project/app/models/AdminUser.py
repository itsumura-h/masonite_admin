"""AdminUser Model"""
"""Model Definition (generated with love by Masonite) 

id: integer default: None
name: string(255) default: None
email: string(255) default: None
password: string(255) default: None
created_at: datetime default: CURRENT_TIMESTAMP
updated_at: datetime default: CURRENT_TIMESTAMP
"""
from config.database import Model


class AdminUser(Model):
    """AdminUser Model"""
    pass