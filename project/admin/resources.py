from masonite.controllers import Controller
from config.database import DB

class AdminController:
    def root(self):
        with open('admin/templates/index.html', 'r') as f:
            return f.read()
