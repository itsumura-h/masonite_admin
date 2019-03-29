from masonite.routes import Get, Post, Patch, Delete
from .resources import AdminController
# from api.resources import Resource
# from api.serializers import JSONSerializer


# class UserResource(Resource, JSONSerializer):
#     model = User

# class PostResource(Resource, JSONSerializer):
#     model = Post


ADMIN_PACKAGE_ROUTES = [
    Get().route('/', AdminController.root),
    Get().route('/api/tables',AdminController.tables),
    Get().route('/@table', AdminController.root),
    Get().route('/@table/@id/edit', AdminController.root),
    Get().route('/@table/@id', AdminController.root),
    
    
    #UserResource('/api/users').routes(),
    #PostResource('/api/posts').routes(),
]
