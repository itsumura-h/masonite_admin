"""Web Routes."""

from masonite.routes import Get, Post, RouteGroup

ROUTES = [
    Get('/', 'WelcomeController@show').name('welcome'),
]

from admin.web.admin_routes import (
    ADMIN_ROUTES,
    ADMIN_ROUTES_WITH_MIDDLEWARE,
    ADMIN_ROUTES_ONLY_ADMINISTRATOR,
    MODEL_ROUTES
)

ROUTES += [
    RouteGroup(ADMIN_ROUTES_WITH_MIDDLEWARE, prefix='/admin', middleware=('admin',), add_methods=['OPTIONS']),
    RouteGroup(ADMIN_ROUTES_ONLY_ADMINISTRATOR, prefix='/admin', middleware=('admin','administrator',), add_methods=['OPTIONS']),
    RouteGroup(MODEL_ROUTES, prefix='/admin', middleware=('admin_model',), add_methods=['OPTIONS']), #middleware not working
    RouteGroup(ADMIN_ROUTES, prefix='/admin', add_methods=['OPTIONS']),
]
