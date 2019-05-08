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
        return self._schema(self, request)

    @staticmethod
    def _schema(self, request: Request):
        model_name = request.param('model')
        table_name = inflection.tableize(model_name)
        row = self.get_model_row_by_model_name(model_name)

        #pprint.pprint(inspect.getmembers(row['model']))
        model_i = row['model']()
        table = model_i.get_table()

        if env('DB_CONNECTION') == 'sqlite':
            # Get Schema in SQLite with Python
            # https://www.tomordonez.com/get-schema-sqlite-python.html
            db = sqlite3.connect(env('DB_DATABASE'))
            cursor = db.cursor()

            cursor.execute(f"PRAGMA table_info('{table_name}')")
            schema = cursor.fetchall()

            cursor.execute(f"PRAGMA foreign_key_list('{table_name}')")
            foreign_list = cursor.fetchall()

        # foreign key
        foreign = {}
        for row in foreign_list:
            data = self.foreign_data(self, row[2])
            foreign[row[3]] = data

        return {'schema': schema, 'foreign_keys': foreign}

    def create_display(self, request: Request):
        try:
            model = request.param('model')
            row = self.get_model_row_by_model_name(model)
            create_display = row['create_display']
            return create_display
        except:
            return []

    def create(self, request: Request):
        schema = self._schema(self, request)
        model_name = request.param('model')
        config_model = self.get_model_row_by_model_name(model_name)
        if 'create_display' in config_model and 'id' not in config_model['create_display']:
            config_model['create_display'].insert(0, 'id')

        new_schema = []
        for row in schema['schema']:
            if 'create_display' not in config_model:
                new_schema.append(row)
            elif row[1] in config_model['create_display']:
                new_schema.append(row)

        return {
            'schema': new_schema,
            'foreign_keys': schema['foreign_keys']
        }

    def detail(self, request: Request):
        schema = self._schema(self, request)
        model_name = request.param('model')
        config_model = self.get_model_row_by_model_name(model_name)
        if 'detail_display' in config_model and 'id' not in config_model['detail_display']:
            config_model['detail_display'].insert(0, 'id')

        new_schema = []
        for row in schema['schema']:
            if not 'detail_display' in config_model:
                new_schema.append(row)
            elif row[1] in config_model['detail_display']:
                new_schema.append(row)

        return {
            'schema': new_schema,
            'foreign_keys': schema['foreign_keys']
        }


    @staticmethod
    def foreign_data(self, table_name):
        row = self.get_model_row_by_table_name(table_name)
        try:
            return DB.table(table_name).select('id', row['foreign_display']+' as data').get().serialize()
        except:
            return []

    @staticmethod
    def get_model_row_by_model_name(model_name):
        model = None
        for row in CONFIG:
            if row['model'].__doc__.split(' ')[0] == model_name:
                model = row
                break

        return model

    @staticmethod
    def get_model_row_by_table_name(table_name):
        i = inflection
        model = None
        for row in CONFIG:
            # posts→Post
            if row['model'].__doc__.split(' ')[0] == i.camelize(i.singularize(table_name)):
                model = row
                break

        return model