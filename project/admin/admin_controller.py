from masonite.controllers import Controller
from masonite.request import Request
from config.database import DB, Model

import pprint
from masonite import env
import sqlite3
from api.resources import Resource
from config.admin import CONFIG
import platform
import pkg_resources
from collections import OrderedDict
import inflection
import inspect

class AdminController:
    def root(self):
        with open('admin/templates/admin/build/index.html', 'r') as f:
            return f.read()

    def info(self, request: Request):
        models = []
        for model in CONFIG:
            models.append(model['model'].__doc__.split(' ')[0])

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
        return {'models': models, 'env': env, 'pkg': pkg}

    def schema(self, request: Request):
        model_name = request.param('model')
        table_name = inflection.tableize(model_name)
        model_c = self.get_model_by_name(model_name)

        pprint.pprint(inspect.getmembers(model_c['model']))
        model_i = model_c['model']()
        table = model_i.get_table()
        pprint.pprint(table)

        if env('DB_CONNECTION') == 'sqlite':
            # Get Schema in SQLite with Python
            # https://www.tomordonez.com/get-schema-sqlite-python.html
            db = sqlite3.connect(env('DB_DATABASE'))
            cursor = db.cursor()

            cursor.execute(f"PRAGMA table_info('{table_name}')")
            schema = cursor.fetchall()

            cursor.execute(f"PRAGMA foreign_key_list('{table_name}')")
            foreign = cursor.fetchall()

        return {'schema': schema, 'foreign_key_lists': foreign}

    def foreign(self, request: Request):
        table_name = request.param('table')
        model = self.get_model_by_table_name(table_name)
        try:
            return DB.table(table_name).select('id', model['foreign_display']).get()
        except:
            return []

    @staticmethod
    def get_model_by_model_name(model_name):
        model = None
        for row in CONFIG:
            if row['model'].__doc__.split(' ')[0] == model_name:
                model = row
                break

        return model

    @staticmethod
    def get_model_by_table_name(table_name):
        i = inflection
        model = None
        for row in CONFIG:
            # posts→Post
            if row['model'].__doc__.split(' ')[0] == i.camelize(i.singularize(table_name)):
                model = row
                break

        return model