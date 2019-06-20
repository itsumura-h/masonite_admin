"""
admin conf

MODELS Exmaple
===================================================

from app.User import User
from app.models.Post import Post
MODELS = [
    {
        'model': User,
        'model_str': 'ユーザー一覧',
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

model_str (str): optional
    Displaying name in drawer. It is useful for users who are not English speaker.

create_display (list[str]): optional
    Lists of columns you want to display in create page.

list_display (list[str]): optional
    Lists of columns you want to display in index page.

detail_display (list[str]): optional
    Lists of columns you want to display in show and edit pages.

foreign_display (str): optional
    When model is called through foreign key, this column's data will be displayed as a string.

---
If optional setting is not set, all columns will be displayed.
If foreign_display is not set, primary key will be displayed as a number.

_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_

LOGIN_CONF Exmaple
===================================================

from datetime import timedelta
LOGIN_CONF = {
    'file_path': 'databases/login',
    'timeout': timedelta(hours=1)
}

===================================================

file_path (str): optional
    Define where Login Token Pickle file is.
    if not set, system use 'databases/login3' by default.

timeout (timedelta): optional
    Define how much time server is not access
    if not set, system use '1 hour' by default.
"""

from app.User import User
from app.models.Post import Post
from app.models.Sample import Sample
MODELS = [
    {
        'model': User,
        'model_str': 'ユーザー一覧',
        'create_display': ['name', 'email'],
        'list_display': ['name', 'email'],
        'detail_display': ['name', 'email'],
        'foreign_display': 'name',
    },
    {
        'model': Post,
        'model_str': 'ポスト',
        'create_display': ['title', 'posts', 'user_id'],
        'list_display': ['title', 'posts'],
        'detail_display': ['title', 'posts', 'user_id'],
        'foreign_display': 'title',
    },
    {
        'model': Sample,
        'model_str': 'サンプル一覧',
        'detail_display': ['date', 'datetime', 'time', 'timestamp'],
        'create_display': ['date', 'datetime', 'time', 'timestamp', 'user_id', 'post_id'],
        'list_display': ['date', 'timestamp', 'created_at'],
    }
]

from datetime import timedelta
LOGIN_CONF = {
    'file_path': 'databases/login.bin',
    'timeout': timedelta(hours=1),
    # 'timeout': timedelta(seconds=30)
    # 'timeout': timedelta(minutes=1),
}