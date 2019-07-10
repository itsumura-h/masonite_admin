
"""Admin Routes."""

from masonite.routes import Get, Post, RouteGroup

# from admin.web.admin_controller import ADMIN_STATIC_DIR_PATH, AdminController
from admin.web.admin_controller import AdminController
from admin.web.admin_resources import AdminResource
from admin.web.login_controller import LoginController
from config.admin import MODELS
from config.storage import STATICFILES

from admin.web.controllers.DisplayStaticController import DisplayStaticController, ADMIN_STATIC_DIR_PATH
from admin.web.controllers.InfoController import InfoController
from admin.web.controllers.SchemaController import SchemaController

STATICFILES[ADMIN_STATIC_DIR_PATH] = '/'

ADMIN_ROUTES_WITH_MIDDLEWARE = [
    Get().route('/api/info',InfoController.show),
    Get().route('/api/schema/@model',SchemaController.schema),
    Get().route('/api/schema/create/@model',SchemaController.schema_in_create),
    Get().route('/api/schema/detail/@model',SchemaController.schema_in_detail),
]

MODEL_ROUTES = []
for model in MODELS:
    args = {}
    if model.get('list_display'):
        args['list_display'] = model['list_display']
    if model.get('detail_display'):
        args['detail_display'] = model['detail_display']

    MODEL_ROUTES.append(AdminResource(model['model'], **args).routes())

ADMIN_ROUTES = [
    Post().route('/api/login', LoginController.store),
    Post().route('/api/logout', LoginController.destroy),
    Get().route('/', DisplayStaticController.show),
    Get().route('/login', DisplayStaticController.show),
    Get().route('/@model', DisplayStaticController.show),
    Get().route('/@model/@id/edit', DisplayStaticController.show),
    Get().route('/@model/@id/create', DisplayStaticController.show),
    Get().route('/@model/@id', DisplayStaticController.show),
]

# ROUTES += [
#     RouteGroup(ADMIN_ROUTES, prefix='/admin')
# ]


"""

from admin.web.admin_routes import ADMIN_ROUTES, ADMIN_ROUTES_WITH_MIDDLEWARE, MODEL_ROUTES

ROUTES += [
    RouteGroup(ADMIN_ROUTES_WITH_MIDDLEWARE, prefix='/admin', middleware=('admin',)),
    RouteGroup(MODEL_ROUTES, prefix='/admin', middleware=('admin_model',)), #middleware not working
    RouteGroup(ADMIN_ROUTES, prefix='/admin'),
]

"""
