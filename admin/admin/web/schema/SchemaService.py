import inflection
from masonite import env
from masonite.request import Request

from admin.web.schema.SchemaRepositry import SchemaRepositry
from config.admin import MODELS
from config.database import DB


class SchemaService:

    # ==================================================
    # Doamin Service
    # ==================================================

    def schema(self, request: Request):
        model_name = request.param('model')
        table_name = inflection.tableize(model_name)
        row = self.get_model_row_by_model_name(model_name)

        if env('DB_CONNECTION') == 'sqlite':
            schema, foreign_list = SchemaRepositry() \
                .get_sqlite_schema(table_name, row)

        elif env('DB_CONNECTION') == 'mysql':
            schema, foreign_list = SchemaRepositry() \
                .get_mysql_schema(table_name, row)

        elif env('DB_CONNECTION') == 'postgres':
            schema, foreign_list = SchemaRepositry() \
                .get_pgsql_schema(table_name, row)

        foreign = {}
        for row in foreign_list:
            data = self.__foreign_data(self, row[2])  # row[2] = table_name
            foreign[row[3]] = data  # row[3] = column_name

        return {'schema': schema, 'foreign_keys': foreign}

    # ==================================================
    # Application Service
    # ==================================================

    @staticmethod
    def __foreign_data(self, table_name):
        row = self.get_model_row_by_table_name(table_name)
        try:
            return DB.table(table_name) \
                .select('id', row['foreign_display']+' as data') \
                .get() \
                .serialize()
        except Exception:
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
