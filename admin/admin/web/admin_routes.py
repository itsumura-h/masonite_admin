"""Admin Routes."""

from masonite.routes import Get, Post, RouteGroup

from admin.web.controllers.ResourceController import ResourceController
from config.admin import MODELS
from config.storage import STATICFILES

from .controllers.DisplayStaticController import (ADMIN_STATIC_DIR_PATH,
                                                  DisplayStaticController)
from .controllers.InfoController import InfoController
from .controllers.LoginController import LoginController
from .controllers.ManageAdminUsersController import ManageAdminUsersController
from .controllers.SchemaController import SchemaController

STATICFILES[ADMIN_STATIC_DIR_PATH] = '/'

ADMIN_ROUTES_WITH_MIDDLEWARE = [
    Get().route('/api/info', InfoController.show),
    Get().route('/api/schema/@model', SchemaController.schema),
    Get().route(
        '/api/schema/create/@model',
        SchemaController.schema_in_create
    ),
    Get().route(
        '/api/schema/detail/@model',
        SchemaController.schema_in_detail
    ),
]

ADMIN_ROUTES_ONLY_ADMINISTRATOR = [
    Get().route('/api/manage_admin_users', ManageAdminUsersController.index),
    Post().route(
        '/api/manage_admin_users',
        ManageAdminUsersController.store
    ),
    Get().route(
        '/api/manage_admin_users/@id',
        ManageAdminUsersController.show
    ),
    Post().route(
        '/api/manage_admin_users/@id/update',
        ManageAdminUsersController.update
    ),
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
