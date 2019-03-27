"""Web Routes."""

from masonite.routes import Get, Post, RouteGroup
from admin.web import ADMIN_ROUTES

ROUTES = [
    RouteGroup(ADMIN_ROUTES, prefix='/admin'),

    Get().route('/', 'WelcomeController@show').name('welcome'),
]
