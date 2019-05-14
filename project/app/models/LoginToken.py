"""LoginToken Model"""
"""Model Definition (generated with love by Masonite) 

admin_user_id: integer default: None
token: string(255) default: None
created_at: datetime default: CURRENT_TIMESTAMP
updated_at: datetime default: CURRENT_TIMESTAMP
"""
from config.database import Model


class LoginToken(Model):
    """LoginToken Model"""
    pass