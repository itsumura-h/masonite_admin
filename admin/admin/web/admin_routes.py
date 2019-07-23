"""Admin Routes."""

from masonite.routes import Get, Post, RouteGroup

from admin.web.controllers.ResourceController import ResourceController
from config.admin import MODELS
from config.storage import STATICFILES

from admin.web.controllers.DisplayStaticController import DisplayStaticController, ADMIN_STATIC_DIR_PATH
from admin.web.controllers.InfoController import InfoController
from admin.web.controllers.SchemaController import SchemaController
from admin.web.controllers.LoginController import LoginController
from admin.web.controllers.AdminUsersController import AdminUsersController

STATICFILES[ADMIN_STATIC_DIR_PATH] = '/'

ADMIN_ROUTES_WITH_MIDDLEWARE = [
    Get().route('/api/info',InfoController.show),
    Get().route('/api/schema/@model',SchemaController.schema),
    Get().route('/api/schema/create/@model',SchemaController.schema_in_create),
    Get().route('/api/schema/detail/@model',SchemaController.schema_in_detail),
    Get().route('/api/admin_users',AdminUsersController.index),
    Post().route('/api/admin_users/create',AdminUsersController.create),
    Get().route('/api/admin_users/@id',AdminUsersController.show),
]

MODEL_ROUTES = []
for model in MODELS:
    args = {}
    if model.get('list_display'):
        args['list_display'] = model['list_display']
    if model.get('detail_display'):
        args['detail_display'] = model['detail_display']

    MODEL_ROUTES.append(ResourceController(model['model'], **args).routes())

ADMIN_ROUTES = [
    Post().route('/api/login', LoginController.store),
    Post().route('/api/logout', LoginController.destroy),
    Get().route('/', DisplayStaticController.show),
    Get().route('/login', DisplayStaticController.show),
    Get().route('/@model', DisplayStaticController.show),
    Get().route('/@model/create', DisplayStaticController.show),
    Get().route('/@model/@id', DisplayStaticController.show),
    Get().route('/@model/@id/edit', DisplayStaticController.show),
]
