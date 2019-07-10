import inflection
from masonite import env

if env('DB_CONNECTION') == 'mysql':
    import pymysql
    from .field_list import MYSQL_FIELD_TYPE
elif env('DB_CONNECTION') == 'postgres':
    import psycopg2
    from .field_list import PGSQL_FIELD_TYPE
else:
    import sqlite3


class SchemaRepositry:
    def get_sqlite_schema(self, table_name, row):
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
        return schema, foreign_list

    def get_mysql_schema(self, table_name, row):
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
                row_in_foreign_list = [0, 0, 'table', 'key']
                if 'FOREIGN KEY' in data:
                    row = data.split('`')
                    row_in_foreign_list[3] = row[3]
                    row_in_foreign_list[2] = row[5]
                    foreign_list += [row_in_foreign_list]

        return schema, foreign_list

    def get_pgsql_schema(self, table_name, row):
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
                new_row = {'id': i, 'column': row[0], 'type': row[1].split(' ')[
                    0]}
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
                    foreign_list += [(i, 0,
                                      inflection.pluralize(key_name.strip('_id')), key_name)]

        return schema, foreign_list
