from masonite.routes import Get, Post, Patch, Delete
from .admin_controller import AdminController
from admin.admin_resources import AdminResource
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
    args = {}
    if model.get('list_display'):
        args['list_display'] = model['list_display']
    if model.get('detail_display'):
        args['detail_display'] = model['detail_display']

    ADMIN_ROUTES.append(AdminResource(model['model'], **args).routes())

ADMIN_ROUTES += [
    Get().route('/', AdminController.root),
    Get().route('/api/info',AdminController.info),
    Get().route('/api/schema/@model',AdminController.schema),
    Get().route('/api/schema/@model/create',AdminController.create),
    Get().route('/api/schema/@model/detail',AdminController.detail),
    Get().route('/api/create_display/@model', AdminController.create_display),
    Get().route('/@model', AdminController.root),
    Get().route('/@model/@id/edit', AdminController.root),
    Get().route('/@model/@id', AdminController.root),

    #UserResource('/api/users').routes(),
    #PostResource('/api/posts').routes(),
]
