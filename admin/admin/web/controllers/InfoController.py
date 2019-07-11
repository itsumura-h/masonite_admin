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

        env = {}
        env['Python_version'] = platform.python_version() if platform.python_version() else ''
        env['Masonite_version'] = str(pkg_resources.working_set.by_key['masonite']) if str(pkg_resources.working_set.by_key['masonite']) else ''
        env['APP_NAME'] = request.environ['APP_NAME'] if 'APP_NAME' in request.environ else ''
        env['Uname'] = request.environ['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in request.environ else ''
        env['Server'] = request.environ['SERVER_SOFTWARE'] if 'SERVER_SOFTWARE' in request.environ else ''
        env['Timezone'] = datetime.now(tz.tzlocal()).tzname() if datetime.now(tz.tzlocal()).tzname() else ''
        env['Env'] = request.environ['APP_ENV'] if 'APP_ENV' in request.environ else ''

        pkg = {}
        for dist in pkg_resources.working_set:
            pkg[dist.project_name] = dist.version
        pkg = OrderedDict(sorted(pkg.items()))
        return {'models': models, 'env': env, 'pkg': pkg}
