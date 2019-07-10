import os, pathlib

ADMIN_STATIC_DIR_PATH = pathlib.Path(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../templates/admin/build'))

class DisplayStaticController:
    def show(self):
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../templates/admin/build/index.html'), 'r') as f:
            return f.read()
