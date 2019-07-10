import platform
from collections import OrderedDict
from datetime import datetime

import pkg_resources
from dateutil import tz
from masonite.request import Request

from config.admin import MODELS


class InfoController:
    def show(self, request:Request):
        models = []
        for model in MODELS:
            model_en = model['model'].__doc__.split(' ')[0]
            if 'model_str' in model:
                models += [{'en': model_en, 'str': model['model_str']}]
            else:
                models += [{'en': model_en, 'str': model_en}]

        env = {
            'Python_version': platform.python_version(),
            'Masonite_version': str(pkg_resources.working_set.by_key['masonite']),
            'APP_NAME': request.environ['APP_NAME'],
            'Uname': request.environ['HTTP_USER_AGENT'],
            'Server': request.environ['SERVER_SOFTWARE'],
            'Timezone': datetime.now(tz.tzlocal()).tzname(),
            'Env': request.environ['APP_ENV']
        }

        pkg = {}
        for dist in pkg_resources.working_set:
            pkg[dist.project_name] = dist.version
        pkg = OrderedDict(sorted(pkg.items()))
        return {'models': models, 'env': env, 'pkg': pkg}
