from masonite.controllers import Controller
from config.database import DB

class AdminController:
    def root(self):
        with open('admin/templates/index.html', 'r') as f:
            return f.read()


# from masonite.routes import BaseHttpRoute
# from api.resources import Resource
# from api.serializers import JSONSerializer

# class AdminResource(Resource, JSONSerializer, BaseHttpRoute):
#     def __init__(self, model, url=None, method_type='GET'):
#         self.model = model
#         self.route_url = '/admin/api/'
#         print(model.__table__)