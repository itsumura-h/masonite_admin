"""Web Routes."""

from masonite.routes import Get, Post, RouteGroup

ROUTES = [
    Get('/', 'WelcomeController@show').name('welcome'),
]

from admin.web.admin_routes import ADMIN_ROUTES, ADMIN_ROUTES_WITH_MIDDLEWARE, MODEL_ROUTES

ROUTES += [
    RouteGroup(ADMIN_ROUTES_WITH_MIDDLEWARE, prefix='/admin', middleware=('admin',)),
    RouteGroup(MODEL_ROUTES, prefix='/admin', middleware=('admin_model',)), #middleware not working
    RouteGroup(ADMIN_ROUTES, prefix='/admin'),
]
