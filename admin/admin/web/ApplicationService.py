from typing import Dict


class ApplicationService:
    @staticmethod
    def delete_login_params(params: Dict) -> Dict:
        """delete login params from request params

        Args:
            params (Dict{str: str}): including login_id, login_token and login_permission

        Returns:
            Dict: params which is not contain login_id, login_token and login_permission
        """
        del params['login_id'], params['login_token'], params['login_permission']

        if '__token' in params:
            del params['__token']

        return params