"""User Model."""
"""Model Definition (generated with love by Masonite) 

id: integer default: None
name: string(255) default: None
email: string(255) default: None
password: string(255) default: None
remember_token: string(255) default: None
verified_at: datetime default: None
created_at: datetime default: CURRENT_TIMESTAMP
updated_at: datetime default: CURRENT_TIMESTAMP
"""
from config.database import Model


class User(Model):
    """User Model."""

    __fillable__ = ['name', 'email', 'password']

    __auth__ = 'email'
