import re

import pkg_resources
from api.serializers import JSONSerializer
from masonite.exceptions import InvalidRouteCompileException
from masonite.request import Request
from masonite.routes import BaseHttpRoute, Route

from admin.web.Resource.ResourceDomainService import ResourceDomainService


class ResourceController(BaseHttpRoute, JSONSerializer):
    methods = ['create', 'index', 'count',
               'show', 'update', 'delete', 'options']
    prefix = ''

    def __init__(self, model, url='', create_display=[], list_display=[], detail_display=[], without=[], method_type=['GET'], request=Request):
        self.base_url = model.__doc__.split(' ')[0]  # Model name
        self.route_url = '/api/' + url  # /api/model_name/ /api/model_name/@id
        self.method_type = method_type
        self.named_route = None
        self.list_middleware = []
        self.model = model
        self.model.__hidden__ = without
        self.create_display = create_display
        self.list_display = list_display
        self.detail_display = detail_display
        self.request = request

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
            routes.append(self.__class__(self.model, url=self.base_url,
                                        method_type=['POST']))
        if 'index' in self.methods:
            routes.append(self.__class__(self.model, url=self.base_url,
                                        list_display=self.list_display, method_type=['GET']))
        if 'count' in self.methods:
            routes.append(self.__class__(self.model, url=f'{self.base_url}/count',
                                        list_display=self.list_display, method_type=['GET']))
        if 'show' in self.methods:
            routes.append(self.__class__(self.model, url=f'{self.base_url}/@id',
                                        detail_display=self.detail_display, method_type=['GET']))
        if 'update' in self.methods:
            routes.append(self.__class__(self.model, url=f'{self.base_url}/@id/put',
                                        method_type=['POST']))
        if 'delete' in self.methods:
            routes.append(self.__class__(self.model, url=f'{self.base_url}/@id/delete',
                                        method_type=['POST']))

        if 'options' in self.methods:
            routes.append(self.__class__(self.model, url=f'{self.base_url}/@id',
                                        method_type=['OPTIONS']))

        return routes

    def get_response(self):
        """Gets the response that should be returned from this resource."""

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

            resource_args = {
                'model': self.model,
                'create_display': self.create_display,
                'list_display': self.list_display,
                'detail_display': self.detail_display
            }

            respurce_domain_service = ResourceDomainService(**resource_args)

            if 'POST' in self.method_type and 'put' in self.route_url:
                response = self.request.app().resolve(getattr(respurce_domain_service, 'update'))
            elif 'POST' in self.method_type and 'delete' in self.route_url:
                response = self.request.app().resolve(getattr(respurce_domain_service, 'delete'))
            elif 'POST' in self.method_type:
                response = self.request.app().resolve(getattr(respurce_domain_service, 'create'))
            elif 'GET' in self.method_type and '@' in self.route_url:
                response = self.request.app().resolve(getattr(respurce_domain_service, 'show'))
            elif 'GET' in self.method_type and 'count' in self.route_url:
                response = self.request.app().resolve(getattr(respurce_domain_service, 'count'))
            elif 'GET' in self.method_type:
                response = self.request.app().resolve(getattr(respurce_domain_service, 'index'))
            elif 'OPTIONS' in self.method_type:
                response = self.request.app().resolve(getattr(respurce_domain_service, 'options'))

        # If the resource needs it's own serializer method
        if hasattr(self, 'serialize'):
            response = self.serialize(response)
        # If the resource needs it's own serializer method
        if hasattr(self, 'filter'):
            response = self.filter(response)

        return response

    def run_middleware(self, middleware_type):
        """Runs any middleware necessary for this resource.

        Arguments:
            middleware_type {string} -- Either 'before' or 'after'
        """
        pass

    def load_request(self, request):
        self.request = request
        return self

    def compile_route_to_regex(self, router=None):
        masonite_version = str(
            pkg_resources.working_set.by_key['masonite']).split(' ')[1]
        miner_ver = masonite_version.split('.')
        del miner_ver[2]
        miner_ver = '.'.join(miner_ver)

        if miner_ver == '2.1':
            """Compiles this resource url to a regex pattern."""
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
        else:
            """Compile the given route to a regex string.

            Arguments:
                route {string} -- URI of the route to compile.

            Returns:
                string -- Compiled URI string.
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
                            regex += Route.route_compilers[regex_route.split(':')[
                                1]]
                        except KeyError:
                            raise InvalidRouteCompileException(
                                'Route compiler "{}" is not an available route compiler. '
                                'Verify you spelled it correctly or that you have added it using the compile() method.'.format(
                                    regex_route.split(':')[1])
                            )
                    else:
                        regex += Route.route_compilers['default']

                    regex += r'\/'

                    # append the variable name passed @(variable):int to a list
                    url_list.append(
                        regex_route.replace('@', '').split(':')[0]
                    )
                else:
                    regex += regex_route + r'\/'

            self.url_list = url_list
            regex += '$'

            self._compiled_regex = re.compile(regex.replace(r'\/$', r'$'))
            self._compiled_regex_end = re.compile(regex)

            return regex
