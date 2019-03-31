from masonite.routes import Get, Post, Patch, Delete
from .resources import AdminController
from admin.resources import AdminResource
# from api.resources import Resource
# from api.serializers import JSONSerializer


# class UserResource(Resource, JSONSerializer):
#     model = User

# class PostResource(Resource, JSONSerializer):
#     model = Post

ADMIN_ROUTES = []

from config.admin import CONFIG
for model in CONFIG:
    ADMIN_ROUTES.append(AdminResource(model['model'], model['table']).routes())

ADMIN_ROUTES += [
    Get().route('/', AdminController.root),
    Get().route('/api/tables',AdminController.tables),
    Get().route('/api/schema/@table',AdminController.schema),
    Get().route('/@table', AdminController.root),
    Get().route('/@table/@id/edit', AdminController.root),
    Get().route('/@table/@id', AdminController.root),
    
    
    #UserResource('/api/users').routes(),
    #PostResource('/api/posts').routes(),
]
