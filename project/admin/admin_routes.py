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
    if model.get('list_display') and model.get('detail_display'):
        ADMIN_ROUTES.append(AdminResource(
            model['model'],
            list_display=model['list_display'],
            detail_display=model['detail_display']
        ).routes())
    elif model.get('list_display'):
        ADMIN_ROUTES.append(AdminResource(
            model['model'],
            list_display=model['list_display']
        ).routes())
    elif model.get('detail_display'):
        ADMIN_ROUTES.append(AdminResource(
            model['model'],
            detail_display=model['detail_display']
        ).routes())
    else:
        ADMIN_ROUTES.append(AdminResource(model['model']).routes())

ADMIN_ROUTES += [
    Get().route('/', AdminController.root),
    Get().route('/api/info',AdminController.info),
    Get().route('/api/schema/@model',AdminController.schema),
    Get().route('/@model', AdminController.root),
    Get().route('/@model/@id/edit', AdminController.root),
    Get().route('/@model/@id', AdminController.root),

    #UserResource('/api/users').routes(),
    #PostResource('/api/posts').routes(),
]