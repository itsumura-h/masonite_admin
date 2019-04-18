from masonite.routes import BaseHttpRoute
from api.serializers import JSONSerializer
from masonite.request import Request
from api.exceptions import (ApiNotAuthenticated, ExpiredToken, InvalidToken,
                            NoApiTokenFound, PermissionScopeDenied,
                            RateLimitReached)
class AdminResource(BaseHttpRoute, JSONSerializer):
    methods = ['create', 'index', 'show', 'update', 'delete', 'options']
    prefix = ''

    def __init__(self, model, url, list_display=[] , without=[], method_type=['GET']):
        self.base_url = url
        self.route_url = '/api/' + url
        self.method_type = method_type
        self.named_route = None
        self.list_middleware = []
        self.model = model
        self.model.__hidden__ = without
        self.list_display = list_display

    def routes(self):
        routes = []
        # if 'create' in self.methods:
        #     routes.append(self.__class__(self.model, self.base_url, method_type=['POST']))
        # if 'index' in self.methods:
        #     routes.append(self.__class__(self.model, self.base_url, list_display=self.list_display, method_type=['GET']))
        # if 'show' in self.methods:
        #     routes.append(self.__class__(self.model, self.base_url + '/@id', method_type=['GET']))
        # if 'update' in self.methods:
        #     routes.append(self.__class__(self.model, self.base_url + '/@id', method_type=['PUT']))
        # if 'delete' in self.methods:
        #     routes.append(self.__class__(self.model, self.base_url + '/@id', method_type=['DELETE']))
        if 'create' in self.methods:
            routes.append(self.__class__(self.model, self.base_url, method_type=['POST']))
        if 'index' in self.methods:
            routes.append(self.__class__(self.model, self.base_url, list_display=self.list_display, method_type=['GET']))
        if 'show' in self.methods:
            routes.append(self.__class__(self.model, self.base_url + '/@id', method_type=['GET']))
        if 'update' in self.methods:
            routes.append(self.__class__(self.model, self.base_url + '/@id/patch', method_type=['POST']))
        if 'delete' in self.methods:
            routes.append(self.__class__(self.model, self.base_url + '/@id/delete', method_type=['POST']))

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

    def create(self):
        """Logic to create data from a given model
        """
        try:
            record = self.model.create(self.request.all())
        except Exception as e:
            return {'error': str(e)}
        return record

    def index(self):
        """Logic to read data from several models
        """
        if self.list_display:
            return self.model.select('id', *self.list_display).get()
        else:
            return self.model.all()

    def show(self, request: Request):
        """Logic to read data from 1 model
        """
        return self.model.find(request.param('id'))

    def update(self, request: Request):
        """Logic to update data from a given model
        """
        record = self.model.find(request.param('id'))
        record.update(request.all())
        return record

    def delete(self, request: Request):
        """Logic to delete data from a given model
        """
        record = self.model.find(request.param('id'))
        if record:
            record.delete()
            return record

        return {'error': 'Record does not exist'}
