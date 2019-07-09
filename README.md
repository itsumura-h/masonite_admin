Masonite Admin
===

## How to install
1.pip install

```
# pip install --editable .
pip install "git+https://github.com/itsumura-h/masonite_admin.git@admin#subdirectory=admin"
```

2.Add some scripts

config/providers.py
```
from admin.providers import AdminProvider
PROVIDERS += [AdminProvider]
```

routes/web.py
```
from masonite.routes import Get, Post, RouteGroup
```

3.Run install command
```
craft admin:install
```

4.Run migrate
```
craft migrate
```

5.Create admin account
```
craft admin:createsuperuser
```

6.Edit admin config file
config/admin.py

7.Run server and access admin page
```
craft serve
```

http://localhost:8000/admin/login

## Commands
- admin:install
Activate admin site automatically.

- admin:createsuperuser
Create account to login admin page.