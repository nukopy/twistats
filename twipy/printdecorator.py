# decorator
def print_params(param_name: str):
    # requestのパラメータを設定 + パラメータの中身を出力する関数にデコレート
    def _print_params(func):
        def wrapper(*args, **kwargs):
            param = func(*args, **kwargs)
            # print
            print('current {} param'.format(param_name))
            for key, value in param.items():
                print('{}: {}'.format(key, value))
            print('-'*10 + '\n')
            return param
        return wrapper
    return _print_params


def print_status_code(http_method: str):
    # responseを返す + ステータスコードを出力をする関数にデコレート
    def _print_status_code(func):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            if response.status_code == 200:
                print('{} succeed'.format(http_method))
                print('HTTP status code: {}'.format(response.status_code))
            else:
                print('{} failed'.format(http_method))
                print('HTTP status code: {}'.format(response.status_code))
            return response
        return wrapper
    return _print_status_code
