from masonite.controllers import Controller
from masonite.request import Request
from config.database import DB

import pprint
from masonite import env
import sqlite3
from api.resources import Resource
from config.admin import CONFIG
import platform
import pkg_resources
from collections import OrderedDict

class AdminController:
    def root(self):
        # with open('admin/templates/index.html', 'r') as f:
        #     return f.read()
        with open('admin/templates/admin/build/index.html', 'r') as f:
            return f.read()

    def tables(self, request: Request):
        tables = {}
        for model in CONFIG:
            tables[model['model'].__name__] = model['table']

        env = {
            'Python_version': platform.python_version(),
            'Masonite_version': str(pkg_resources.working_set.by_key['masonite']),
            'APP_NAME': request.environ['APP_NAME'],
            'Uname': request.environ['HTTP_USER_AGENT'],
            'Server': request.environ['SERVER_SOFTWARE'],
            'Locale': request.environ['LANGUAGE'],
            'Env': request.environ['APP_ENV']
        }

        pkg = {}
        for dist in pkg_resources.working_set:
            pkg[dist.project_name] = dist.version
        pkg = OrderedDict(sorted(pkg.items()))
        return {'tables': tables, 'env': env, 'pkg': pkg}

    def schema(self, request: Request):
        table = request.param('table')
        if env('DB_CONNECTION') == 'sqlite':
            # Get Schema in SQLite with Python
            # https://www.tomordonez.com/get-schema-sqlite-python.html
            db = sqlite3.connect(env('DB_DATABASE'))
            cursor = db.cursor()
            cursor.execute(f"PRAGMA table_info('{table}')")
            schema = cursor.fetchall()

        return schema