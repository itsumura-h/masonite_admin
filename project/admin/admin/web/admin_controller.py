from masonite.controllers import Controller
from masonite.request import Request
from config.database import DB, Model

from masonite import env
import sqlite3
from api.resources import Resource
from config.admin import MODELS
import platform
import pkg_resources
from collections import OrderedDict
import inflection
import inspect
from datetime import datetime
from dateutil import tz

if env('DB_CONNECTION') == 'mysql':
    import pymysql
    # pip install mysql-connector-python-rf
    from .mysql_field_list import FIELD_TYPE

from pprint import pprint

class AdminController:
    def root(self):
        with open('admin/admin/templates/admin/build/index.html', 'r') as f:
            return f.read()

    def info(self, request: Request):
        models = []
        for model in MODELS:
            models.append(model['model'].__doc__.split(' ')[0])

        env = {
            'Python_version': platform.python_version(),
            'Masonite_version': str(pkg_resources.working_set.by_key['masonite']),
            'APP_NAME': request.environ['APP_NAME'],
            'Uname': request.environ['HTTP_USER_AGENT'],
            'Server': request.environ['SERVER_SOFTWARE'],
            'Timezone': datetime.now(tz.tzlocal()).tzname(),
            'Env': request.environ['APP_ENV']
        }

        pkg = {}
        for dist in pkg_resources.working_set:
            pkg[dist.project_name] = dist.version
        pkg = OrderedDict(sorted(pkg.items()))
        return {'models': models, 'env': env, 'pkg': pkg}

    def schema(self, request: Request):
        return self._schema(self, request)

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
        if 'create_display' in config_model and 'id' in config_model['create_display']:
            config_model['create_display'].remove('id')

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
    def _schema(self, request: Request):
        model_name = request.param('model')
        table_name = inflection.tableize(model_name)
        row = self.get_model_row_by_model_name(model_name)

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

        elif env('DB_CONNECTION') == 'mysql':
            conn = pymysql.connect(host=env('DB_HOST'),
                    user=env('DB_USERNAME'),
                    password=env('DB_PASSWORD'),
                    db=env('DB_DATABASE'),
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)

            with conn.cursor() as cursor:
                sql = f"SELECT * FROM {table_name} LIMIT 1"
                cursor.execute(sql)
                schema = cursor.description
                schema = list(schema)
                i = 0
                for row in schema:
                    row = list(row)
                    for k, v in FIELD_TYPE.items():
                        if str(row[1]) == k:
                            row[1] = v
                    schema[i] = row
                    i += 1

            foreign_list = []
            with conn.cursor() as cursor:
                sql = f"SHOW CREATE TABLE {table_name}"
                cursor.execute(sql)
                filedata = cursor.fetchone()['Create Table']
                filedata_arr = filedata.splitlines()
                row_in_foreign_list = [0,0,'table','key']
                for data in filedata_arr:
                    if 'FOREIGN KEY' in data:
                        row = data.split('`')
                        row_in_foreign_list[3] = row[3]
                        row_in_foreign_list[2] = row[5]
                        foreign_list += [row_in_foreign_list]

        foreign = {}
        for row in foreign_list:
            data = self.foreign_data(self, row[2])
            foreign[row[3]] = data

        return {'schema': schema, 'foreign_keys': foreign}

    @staticmethod
    def foreign_data(self, table_name):
        row = self.get_model_row_by_table_name(table_name)
        print(row)
        try:
            return DB.table(table_name).select('id', row['foreign_display']+' as data').get().serialize()
        except:
            return []

    @staticmethod
    def get_model_row_by_model_name(model_name):
        model = None
        for row in MODELS:
            if row['model'].__doc__.split(' ')[0] == model_name:
                model = row
                break

        return model

    @staticmethod
    def get_model_row_by_table_name(table_name):
        i = inflection
        model = None
        for row in MODELS:
            # posts→Post
            if row['model'].__doc__.split(' ')[0] == i.camelize(i.singularize(table_name)):
                model = row
                break

        return model