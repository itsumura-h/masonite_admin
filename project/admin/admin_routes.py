from masonite.routes import RouteGroup
from .resources import AdminResource
from app.User import User
from app.models.Post import Post
from admin.admin_package_routes import ADMIN_PACKAGE_ROUTES

ADMIN_ROUTES = [
    AdminResource(User, 'users', without=['password']).routes(),
    AdminResource(Post, 'posts').routes(),
    RouteGroup(ADMIN_PACKAGE_ROUTES),
]
