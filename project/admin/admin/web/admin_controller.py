import inspect, os, pathlib, platform, sqlite3
from collections import OrderedDict
from datetime import datetime
from pprint import pprint

import inflection
import pkg_resources
from api.resources import Resource
from dateutil import tz
from masonite import env
from masonite.controllers import Controller
from masonite.request import Request

from config.admin import MODELS
from config.database import DB, Model

if env('DB_CONNECTION') == 'mysql':
    import pymysql
    from .field_list import MYSQL_FIELD_TYPE
elif env('DB_CONNECTION') == 'postgres':
    import psycopg2
    from .field_list import PGSQL_FIELD_TYPE

ADMIN_STATIC_DIR_PATH = pathlib.Path(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../templates/admin/build/static'))

class AdminController:
    def root(self):
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../templates/admin/build/index.html'), 'r') as f:
            return f.read()

    def info(self, request: Request):
        models = []
        for model in MODELS:
            model_en = model['model'].__doc__.split(' ')[0]
            if 'model_str' in model:
                models += [{'en': model_en, 'str': model['model_str']}]
            else:
                models += [{'en': model_en, 'str': model_en}]

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

        if 'create_display' in config_model:
            new_schema = [v for i, v in enumerate(schema['schema']) if v['column'] in config_model['create_display']]
        else:
            new_schema = [v for i, v in enumerate(schema['schema']) if v['column'] not in ['id', 'created_at', 'updated_at'] ]

        return {
            'schema': new_schema,
            'foreign_keys': schema['foreign_keys']
        }

    def detail(self, request: Request):
        schema = self._schema(self, request)
        model_name = request.param('model')
        config_model = self.get_model_row_by_model_name(model_name)
        if 'id' not in config_model['detail_display']:
            config_model['detail_display'].insert(0, 'id')

        if 'detail_display' in config_model:
            new_schema = [v for i, v in enumerate(schema['schema']) if v['column'] in config_model['detail_display']]
        else:
            new_schema = [v for i, v in enumerate(schema['schema']) if v['column'] not in ['created_at', 'updated_at'] ]

        return {
            'schema': new_schema,
            'foreign_keys': schema['foreign_keys']
        }

    @staticmethod
    def _schema(self, request: Request):
        model_name = request.param('model')
        table_name = inflection.tableize(model_name)
        row = self.get_model_row_by_model_name(model_name)

        #model_i = row['model']()
        #table = model_i.get_table()

        if env('DB_CONNECTION') == 'sqlite':
            # Get Schema in SQLite with Python
            # https://www.tomordonez.com/get-schema-sqlite-python.html
            db = sqlite3.connect(env('DB_DATABASE'))
            cursor = db.cursor()

            cursor.execute(f"PRAGMA table_info('{table_name}')")
            schema = list(cursor.fetchall())
            for i, row in enumerate(schema):
                row = list(row)
                schema[i] = {'id': row[0], 'column': row[1], 'type': row[2]}

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
                sql = f'SELECT * FROM {table_name} LIMIT 1'
                cursor.execute(sql)
                schema = cursor.description
                schema = list(schema)

                for i, row in enumerate(schema):
                    new_row = {'id': i, 'column': row[0], 'type': row[1]}
                    for k, v in MYSQL_FIELD_TYPE.items():
                        if str(new_row['type']) == k:
                            new_row['type'] = v
                    schema[i] = new_row

            foreign_list = []
            with conn.cursor() as cursor:
                sql = f'SHOW CREATE TABLE {table_name}'
                cursor.execute(sql)
                filedata = cursor.fetchone()['Create Table']
                filedata_arr = filedata.splitlines()
                for data in filedata_arr:
                    row_in_foreign_list = [0,0,'table','key']
                    if 'FOREIGN KEY' in data:
                        row = data.split('`')
                        row_in_foreign_list[3] = row[3]
                        row_in_foreign_list[2] = row[5]
                        foreign_list += [row_in_foreign_list]
        elif env('DB_CONNECTION') == 'postgres':
            conn = psycopg2.connect(host=env('DB_HOST'),
                    database=env('DB_DATABASE'),
                    user=env('DB_USERNAME'),
                    password=env('DB_PASSWORD'),
                    port=env('DB_PORT'))

            with conn.cursor()as cursor:
                sql = f"select column_name, data_type from information_schema.columns where table_name = '{table_name}'"
                cursor.execute(sql)
                schema = cursor.fetchall()
                for i, row in enumerate(schema):
                    new_row = {'id': i, 'column': row[0], 'type': row[1].split(' ')[0]}
                    for k, v in PGSQL_FIELD_TYPE.items():
                        if str(new_row['type']) == k:
                            new_row['type'] = v
                            schema[i] = new_row
                            break

            foreign_list = []
            with conn.cursor() as cursor:
                sql = "SELECT table_name, constraint_name FROM information_schema.table_constraints WHERE table_schema = 'public' AND constraint_type = 'FOREIGN KEY'"
                cursor.execute(sql)
                filedata = cursor.fetchall()
                for i, v in enumerate(filedata):
                    key_name = v[1]
                    key_name = key_name.replace(f'{table_name}_', '')
                    key_name = key_name.strip('_foreign')

                    if v[0] == table_name:
                        foreign_list += [(i, 0, inflection.pluralize(key_name.strip('_id')), key_name)]

        foreign = {}
        for row in foreign_list:
            data = self.foreign_data(self, row[2]) # row[2] = table_name
            foreign[row[3]] = data # row[3] = column_name

        return {'schema': schema, 'foreign_keys': foreign}

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
