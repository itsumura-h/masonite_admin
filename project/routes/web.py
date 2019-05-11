"""Web Routes."""

from masonite.routes import Get, Post, RouteGroup
#from admin.admin_routes import ADMIN_ROUTES
from admin.web.admin_routes import ADMIN_ROUTES

ROUTES = [
    Get().route('/', 'WelcomeController@show').name('welcome'),
    #RouteGroup(ADMIN_ROUTES, prefix='/admin', add_methods=["OPTIONS"]),
    RouteGroup(ADMIN_ROUTES, prefix='/admin'),
]
