# decorator
import json


def print_params(param_name: str):
    """Output logs of API parameters config"""
    def _print_params(func):
        def wrapper(*args, **kwargs):
            param = func(*args, **kwargs)
            # output
            print('current {} param'.format(param_name))
            for key, value in param.items():
                print('{}: {}'.format(key, value))
            print('-'*10 + '\n')

            return param
        return wrapper
    return _print_params


def print_status_code(http_method: str, api: str):
    """
    Output logs of  response-obj's status_code
    and if a request was failed, return msg(str-type) not JSON-parsed obj.
    """
    def _print_status_code(func):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            status_code = response.status_code

            # log: status_code
            print('----- {} -----'.format(api))
            result = 'succeed' if (status_code == 200) else 'failed'
            msg = f'{http_method} {result}\nHTTP status code: {status_code}\n'
            print(msg)
            if status_code == 200:
                return json.loads(response.text)  # dict-type
            else:
                return msg  # str-type

        return wrapper
    return _print_status_code
