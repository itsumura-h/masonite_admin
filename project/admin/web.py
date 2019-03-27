from masonite.routes import Get, Post, Patch, Delete
from .resources import AdminController

from api.resources import Resource
from api.serializers import JSONSerializer
from app.User import User


class UserResource(Resource, JSONSerializer):
    model = User

ADMIN_ROUTES = [
    Get().route('/', AdminController.root),
    Get().route('/@table', AdminController.root),
    UserResource('/api/users').routes(),
]
