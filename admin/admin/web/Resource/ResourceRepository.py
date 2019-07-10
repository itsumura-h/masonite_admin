from masonite.request import Request
from masonite.response import Response
from masonite import env
from admin.web.Resource.ResourceAppService import ResourceAppService


class ResourceRepository:
    def __init__(self, model, create_display, list_display, detail_display):
        self.model = model
        self.create_display = create_display
        self.list_display = list_display
        self.detail_display = detail_display
        self.request = Request

    def create(self, request: Request, response: Response):
        try:
            params = request.all()
            del params['login_id'], params['login_token'], params['permission']
            new_model = self.model()

            for key, value in params.items():
                try:
                    setattr(new_model, key, value)
                except Exception as e:
                    print(e)

            new_model.save()
        except Exception as e:
            return {'error': str(e)}
        return new_model

    def index(self, request: Request, response: Response):
        # pagenagion
        items = int(request.input('i')) if request.input('i') else 10
        page = int(request.input('p')) if request.input('p') else 1
        _offset = items * (page - 1)

        if self.list_display:
            results = self.model.select('id', *self.list_display) \
                    .offset(_offset) \
                    .limit(items) \
                    .get()

            new_results = [result._original for result in results._items]
            return ResourceAppService().arr_iso_format(new_results)
        else:
            results = self.model.offset(_offset).limit(items).get()
            new_results = [result._original for result in results._items]
            return ResourceAppService().arr_iso_format(new_results)

    def count(self, request: Request, response: Response):
        return {'count': self.model.count()}

    def show(self, request, response: Response):
        if self.detail_display and env('DB_CONNECTION') == 'mysql':
            result = self.model.select(
                *self.detail_display).find(request.param('id'))
            new_result = {i: v for i, v in result._original.items()}
            return ResourceAppService().arr_iso_format(new_result)

        elif self.detail_display:
            if 'id' not in self.detail_display:
                self.detail_display.insert(0, 'id')
            result = self.model.select(
                *self.detail_display).find(request.param('id'))
            new_result = {i: v for i, v in result._original.items()}
            return ResourceAppService().arr_iso_format(new_result)

        else:
            result = self.model.find(request.param('id'))
            new_result = {i: v for i, v in result._original.items()}
            return ResourceAppService().arr_iso_format(new_result)

    def update(self, request: Request, response: Response):
        record = self.model.where('id', request.param('id'))
        params = request.all()
        del params['login_id'], params['login_token'], params['permission']

        try:
            record.update(params)
        except Exception as e:
            return {'error': str(e)}

        return {}

    def delete(self, request: Request, response: Response):
        record = self.model.find(request.param('id'))
        if record:
            record.delete()
            return record

        return {'error': 'Record does not exist'}
