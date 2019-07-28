from masonite.request import Request

from ..domain.services.domain_services.SchemaService import SchemaService


class SchemaController:
    def schema(self, request: Request):
        return SchemaService().schema(request)

    def schema_in_create(self, request: Request):
        schema = SchemaService().schema(request)
        model_name = request.param('model')
        config_model = SchemaService.get_model_row_by_model_name(model_name)

        if 'create_display' in config_model:
            new_schema = [
                v for i, v in enumerate(schema['schema'])
                if v['column'] in config_model['create_display']
            ]
        else:
            new_schema = [
                v for i, v in enumerate(schema['schema'])
                if v['column'] not in ['id', 'created_at', 'updated_at']
            ]

        return {
            'schema': new_schema,
            'foreign_keys': schema['foreign_keys']
        }

    def schema_in_detail(self, request: Request):
        schema = SchemaService().schema(request)
        model_name = request.param('model')
        config_model = SchemaService.get_model_row_by_model_name(model_name)
        if 'id' not in config_model['detail_display']:
            config_model['detail_display'].insert(0, 'id')

        if 'detail_display' in config_model:
            new_schema = [
                v for i, v in enumerate(schema['schema'])
                if v['column'] in config_model['detail_display']
            ]
        else:
            new_schema = [
                v for i, v in enumerate(schema['schema'])
                if v['column'] not in ['created_at', 'updated_at']
            ]

        return {
            'schema': new_schema,
            'foreign_keys': schema['foreign_keys']
        }
