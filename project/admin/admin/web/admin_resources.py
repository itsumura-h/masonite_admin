import json
from datetime import date, datetime, time, timedelta
from inspect import getmembers

import bcrypt
from api.exceptions import (ApiNotAuthenticated, ExpiredToken, InvalidToken,
                            NoApiTokenFound, PermissionScopeDenied,
                            RateLimitReached)
from api.serializers import JSONSerializer
from masonite.request import Request
from masonite.response import Response
from masonite.routes import BaseHttpRoute

from admin.web.admin_controller import AdminController
from app.http.middleware.AdminMiddleware import AdminMiddleware


class AdminResource(BaseHttpRoute, JSONSerializer):
    methods = ['create', 'index', 'count', 'show', 'update', 'delete']
    prefix = ''

    def __init__(self, model, url='', create_display=[], list_display=[], detail_display=[], without=[], method_type=['GET'], request=Request):
        self.base_url = model.__doc__.split(' ')[0] # Model name
        self.route_url = '/api/' + url # /api/model_name/ /api/model_name/@id
        self.method_type = method_type
        self.named_route = None
        self.list_middleware = []
        self.model = model
        self.model.__hidden__ = without
        self.create_display = create_display
        self.list_display = list_display
        self.detail_display = detail_display

    def routes(self):
        routes = []
        # if 'create' in self.methods:
        #     routes.append(self.__class__(self.model, self.base_url, method_type=['POST']))
        # if 'index' in self.methods:
        #     routes.append(self.__class__(self.model, self.base_url, method_type=['GET']))
        # if 'show' in self.methods:
        #     routes.append(self.__class__(self.model, self.base_url + '/@id', method_type=['GET']))
        # if 'update' in self.methods:
        #     routes.append(self.__class__(self.model, self.base_url + '/@id', method_type=['PUT']))
        # if 'delete' in self.methods:
        #     routes.append(self.__class__(self.model, self.base_url + '/@id', method_type=['DELETE']))

        if 'create' in self.methods:
            routes.append(self.__class__(self.model, url=self.base_url, method_type=['POST']))
        if 'index' in self.methods:
            routes.append(self.__class__(self.model, url=self.base_url, list_display=self.list_display, method_type=['GET']))
        if 'count' in self.methods:
            routes.append(self.__class__(self.model, url=self.base_url + '/count', list_display=self.list_display, method_type=['GET']))
        if 'show' in self.methods:
            routes.append(self.__class__(self.model, url=self.base_url + '/@id', detail_display=self.detail_display, method_type=['GET']))
        if 'update' in self.methods:
            routes.append(self.__class__(self.model, url=self.base_url + '/@id/patch', method_type=['POST']))
        if 'delete' in self.methods:
            routes.append(self.__class__(self.model, url=self.base_url + '/@id/delete', method_type=['POST']))

        return routes

    def get_response(self):
        """Gets the response that should be returned from this resource
        """

        response = None

        if hasattr(self, 'authenticate'):
            # Get a response from the authentication method if one exists
            response = self.run_authentication()

        if hasattr(self, 'scope'):
            # Get a response from the authentication method if one exists
            if not response:
                response = self.run_scope()


        # If the authenticate method did not return a response, continue on to one of the CRUD responses
        if not response:
            # if 'POST' in self.method_type:
            #     response = self.request.app().resolve(getattr(self, 'create'))
            # elif 'GET' in self.method_type and '@' in self.route_url:
            #     response = self.request.app().resolve(getattr(self, 'show'))
            # elif 'GET' in self.method_type:
            #     response = self.request.app().resolve(getattr(self, 'index'))
            # elif 'PUT' in self.method_type or 'PATCH' in self.method_type:
            #     response = self.request.app().resolve(getattr(self, 'update'))
            # elif 'DELETE' in self.method_type:
            #     response = self.request.app().resolve(getattr(self, 'delete'))

            if 'POST' in self.method_type and 'patch' in self.route_url:
                response = self.request.app().resolve(getattr(self, 'update'))
            elif 'POST' in self.method_type and 'delete' in self.route_url:
                response = self.request.app().resolve(getattr(self, 'delete'))
            elif 'POST' in self.method_type:
                response = self.request.app().resolve(getattr(self, 'create'))
            elif 'GET' in self.method_type and '@' in self.route_url:
                response = self.request.app().resolve(getattr(self, 'show'))
            elif 'GET' in self.method_type and 'count' in self.route_url:
                response = self.request.app().resolve(getattr(self, 'count'))
            elif 'GET' in self.method_type:
                response = self.request.app().resolve(getattr(self, 'index'))


        # If the resource needs it's own serializer method
        if hasattr(self, 'serialize'):
            response = self.serialize(response)
        # If the resource needs it's own serializer method
        if hasattr(self, 'filter'):
            response = self.filter(response)

        return response

    def run_middleware(self, middleware_type):
        """Runs any middleware necessary for this resource

        Arguments:
            middleware_type {string} -- Either 'before' or 'after'
        """
        pass

    def load_request(self, request):
        self.request = request
        return self

    def compile_route_to_regex(self, router):
        """Compiles this resource url to a regex pattern
        """

        # Split the route
        split_given_route = self.route_url.split('/')
        # compile the provided url into regex
        url_list = []
        regex = '^'
        for regex_route in split_given_route:
            if '@' in regex_route:
                if ':' in regex_route:
                    try:
                        regex += router.route_compilers[regex_route.split(':')[
                            1]]
                    except KeyError:
                        raise InvalidRouteCompileException(
                            'Route compiler "{}" is not an available route compiler. '
                            'Verify you spelled it correctly or that you have added it using the compile() method.'.format(
                                regex_route.split(':')[1])
                        )
                else:
                    regex += router.route_compilers['default']

                regex += r'\/'

                # append the variable name passed @(variable):int to a list
                url_list.append(
                    regex_route.replace('@', '').split(':')[0]
                )
            else:
                regex += regex_route + r'\/'

        router.url_list = url_list
        regex += '$'
        return regex

    def create(self, request: Request, response: Response):
        """Logic to create data from a given model
        """
        if AdminMiddleware(request, response).checkpw_resource() == False:
            return response.json(None, status=403)

        try:
            params = request.all()
            del params['login_id'], params['login_token']
            config_model = AdminController.get_model_row_by_model_name(self.model.__doc__.split(' ')[0])
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

        # try:
        #     record = self.model.create(self.request.all())
        # except Exception as e:
        #     return {'error': str(e)}
        # return record

    def index(self, request: Request, response: Response):
        """Logic to read data from several models
        """
        if AdminMiddleware(request, response).checkpw_resource() == False:
            return response.json(None, status=403)

        # pagenagion
        items = request.input('i') if request.input('i') else 10
        page = request.input('p') if request.input('p') else 1
        _offset = items * (page - 1)

        if self.list_display:
            results = self.model.select('id', *self.list_display).offset(_offset).limit(items).get()
            new_results = [result._original for result in results._items]
            return self.arr_iso_format(new_results)
            #return self.model.select('id', *self.list_display).paginate(items, page).serialize()
        else:
            results = self.model.offset(_offset).limit(items).get()
            new_results = [result._original for result in results._items]
            return self.arr_iso_format(new_results)

        # if self.list_display:
        #     return self.model.select('id', *self.list_display).get()
        # else:
        #     return self.model.all()

    def count(self, request: Request, response: Response):
        if AdminMiddleware(request, response).checkpw_resource() == False:
            return response.json(None, status=403)

        return {'count': self.model.count()}

    def show(self, request: Request, response: Response):
        """Logic to read data from 1 model
        """
        if AdminMiddleware(request, response).checkpw_resource() == False:
            return response.json(None, status=403)

        if self.detail_display and env('DB_CONNECTION') == 'mysql':
            result = self.model.select(*self.detail_display).find(request.param('id'))
            new_result = {i: v for i, v in result._original.items()}
            return self.arr_iso_format(new_result)
        elif self.detail_display:
            if 'id' not in self.detail_display:
                self.detail_display.insert(0, 'id')
            result = self.model.select(*self.detail_display).find(request.param('id'))
            new_result = {i: v for i, v in result._original.items()}
            return self.arr_iso_format(new_result)
        else:
            result = self.model.find(request.param('id'))
            new_result = {i: v for i, v in result._original.items()}
            return self.arr_iso_format(new_result)

    def update(self, request: Request, response: Response):
        """Logic to update data from a given model
        """
        if AdminMiddleware(request, response).checkpw_resource() == False:
            return response.json(None, status=403)

        record = self.model.where('id', request.param('id'))
        params = request.all()
        del params['login_id'], params['login_token']
        try:
            record.update(params)
        except Exception as e:
            return {'error': str(e)}

        return {}#self.model.where('id', request.param('id')).get().serialize()

    def delete(self, request: Request, response: Response):
        """Logic to delete data from a given model
        """
        if AdminMiddleware(request, response).checkpw_resource() == False:
            return response.json(None, status=403)

        record = self.model.find(request.param('id'))
        if record:
            record.delete()
            return record

        return {'error': 'Record does not exist'}


    def arr_iso_format(self, _obj):
        if isinstance(_obj, datetime) or isinstance(_obj, date):
            return _obj.isoformat()
        elif isinstance(_obj, timedelta):
            _obj_arr = str(_obj).split(':')
            return datetime(1970, 1, 2, int(_obj_arr[0]), int(_obj_arr[1]), int(_obj_arr[2])).isoformat()
        elif isinstance(_obj, time):
            _obj_arr = str(_obj).split(':')
            #return _obj.isoformat()
            return datetime(1970, 1, 2, int(_obj_arr[0]), int(_obj_arr[1]), int(_obj_arr[2])).isoformat()
        elif isinstance(_obj, list):
            return [self.arr_iso_format(o) for o in _obj]
        elif isinstance(_obj, dict):
            return {key: self.arr_iso_format(value) for key, value in _obj.items() }
        else:
            return _obj
