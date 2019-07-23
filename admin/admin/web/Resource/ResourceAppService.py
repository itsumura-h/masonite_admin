from datetime import date, datetime, time, timedelta
from app.http.middleware.AdminMiddleware import AdminMiddleware
from typing import Dict

class ResourceAppService:
    # ==================================================
    # Application Service
    # ==================================================

    def arr_iso_format(self, _obj):
        if isinstance(_obj, datetime) or isinstance(_obj, date):
            return _obj.isoformat()
        elif isinstance(_obj, timedelta):
            _obj = str(_obj).split(' ')[2] # "7138 days, 14:32:46.649462"→"14:32:46.649462"
            _obj_arr = str(_obj).split(':') # "14:32:46.649462"→[14, 32, 46.649462]
            _h = int(_obj_arr[0])
            _m = int(_obj_arr[1])
            _s = int(_obj_arr[2].split('.')[0])
            return datetime(1970, 1, 2, _h, _m, _s).isoformat()
        elif isinstance(_obj, time):
            _obj_arr = str(_obj).split(':')
            _h = int(_obj_arr[0])
            _m = int(_obj_arr[1])
            _s = int(_obj_arr[2].split('.')[0])
            return datetime(1970, 1, 2, _h, _m, _s).isoformat()
        elif isinstance(_obj, list):
            return [self.arr_iso_format(o) for o in _obj]
        elif isinstance(_obj, dict):
            return {key: self.arr_iso_format(value) for key, value in _obj.items()}
        else:
            return _obj

    def before_crud_check(self, request, response):
        if AdminMiddleware(request, response).checkpw_resource() is False:
            return False

        login_permission = request.input('login_permission')
        if request.method != 'GET' and login_permission == 'user':
            return False

    # @staticmethod
    # def delete_login_params(params: Dict) -> Dict:
    #     """delete login params from request params

    #     Args:
    #         params (Dict{str: str}): including login_id, login_token and login_permission

    #     Returns:
    #         Dict: params which is not contain login_id, login_token and login_permission
    #     """
    #     del params['login_id'], params['login_token'], params['login_permission']

    #     if '__token' in params:
    #         del params['__token']

    #     return params
