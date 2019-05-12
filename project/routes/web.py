"""Web Routes."""

from masonite.routes import Get, Post, RouteGroup

ROUTES = [
    Get().route('/', 'WelcomeController@show').name('welcome'),
]

# """Admin Routes."""

# from masonite.routes import Get, Post, RouteGroup
# from admin.web.admin_controller import AdminController
# from admin.web.admin_resources import AdminResource
# from admin.web.login_controller import LoginController
# from config.admin import MODELS
# from config.storage import STATICFILES

# STATICFILES['admin/templates/admin/build/static'] = 'static/'

# ADMIN_ROUTES = []
# for model in MODELS:
#     args = {}
#     if model.get('list_display'):
#         args['list_display'] = model['list_display']
#     if model.get('detail_display'):
#         args['detail_display'] = model['detail_display']

#     ADMIN_ROUTES.append(AdminResource(model['model'], **args).routes())

# ADMIN_ROUTES += [
#     Get().route('/', AdminController.root),
#     Get().route('/api/info',AdminController.info),
#     Get().route('/api/schema/@model',AdminController.schema),
#     Get().route('/api/schema/@model/create',AdminController.create),
#     Get().route('/api/schema/@model/detail',AdminController.detail),
#     Get().route('/api/create_display/@model', AdminController.create_display),
#     Post().route('/api/login', LoginController.store),
#     Get().route('/@model', AdminController.root),
#     Get().route('/@model/@id/edit', AdminController.root),
#     Get().route('/@model/@id', AdminController.root),
# ]

# ROUTES += [
#     RouteGroup(ADMIN_ROUTES, prefix='/admin')
# ]
from admin.web.admin_routes import ADMIN_ROUTES

ROUTES += [
    RouteGroup(ADMIN_ROUTES, prefix='/admin')
]
