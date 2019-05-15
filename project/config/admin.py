"""
admin conf

Exmaple
===================================================

from app.User import User
from app.models.Post import Post
MODELS = [
    {
        'model': User,
        'create_display': ['name', 'email'],
        'list_display': ['name', 'email'],
        'detail_display': ['name', 'email'],
        'foreign_display': 'name',
    },
    {
        'model': Post,
        'create_display': ['title', 'posts', 'user_id'],
        'list_display': ['title', 'posts'],
        'detail_display': ['title', 'posts', 'user_id']
    }
]

===================================================

model (ModelClass): required
    Set model class.

create_display (list[str]): optional
    Lists of columns you want to display in create page.

list_display (list[str]): optional
    Lists of columns you want to display in index page.

detail_display (list[str]): optional
    Lists of columns you want to display in show and edit pages.

foreign_display (str): optional
    When model is called through foreign key, this column's data will be displayed as a string.

---

When optional setting is not set, all columns will display.
When foreign_display is not set, primary key will display.

"""

from app.User import User
from app.models.Post import Post
MODELS = [
    {
        'model': User,
        'create_display': ['name', 'email'],
        'list_display': ['name', 'email'],
        'detail_display': ['name', 'email'],
        'foreign_display': 'name',
    },
    {
        'model': Post,
        'create_display': ['title', 'posts', 'user_id'],
        'list_display': ['title', 'posts'],
        'detail_display': ['title', 'posts', 'user_id']
    }
]
