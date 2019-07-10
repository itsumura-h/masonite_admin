from datetime import date, datetime, time, timedelta
from app.http.middleware.AdminMiddleware import AdminMiddleware


class ResourceAppService:
    # ==================================================
    # Application Service
    # ==================================================

    def arr_iso_format(self, _obj):
        if isinstance(_obj, datetime) or isinstance(_obj, date):
            return _obj.isoformat()
        elif isinstance(_obj, timedelta):
            _obj_arr = str(_obj).split(':')
            return datetime(1970, 1, 2, int(_obj_arr[0]), int(_obj_arr[1]), int(_obj_arr[2])).isoformat()
        elif isinstance(_obj, time):
            _obj_arr = str(_obj).split(':')
            return datetime(1970, 1, 2, int(_obj_arr[0]), int(_obj_arr[1]), int(_obj_arr[2])).isoformat()
        elif isinstance(_obj, list):
            return [self.arr_iso_format(o) for o in _obj]
        elif isinstance(_obj, dict):
            return {key: self.arr_iso_format(value) for key, value in _obj.items()}
        else:
            return _obj

    def before_crud_check(self, request, response):
        if AdminMiddleware(request, response).checkpw_resource() is False:
            return False

        permission = request.input('permission')
        if request.method != 'GET' and int(permission) > 2:
            return False
