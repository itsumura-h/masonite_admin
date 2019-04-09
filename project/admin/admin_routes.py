from masonite.routes import Get, Post, Patch, Delete
from .admin_controller import AdminController
from admin.resources import AdminResource
from config.admin import CONFIG
from config.storage import STATICFILES
# from api.resources import Resource
# from api.serializers import JSONSerializer


# class UserResource(Resource, JSONSerializer):
#     model = User

# class PostResource(Resource, JSONSerializer):
#     model = Post

STATICFILES['admin/templates/admin/build/static'] = 'static/'

ADMIN_ROUTES = []
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
