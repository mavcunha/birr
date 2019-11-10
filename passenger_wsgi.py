from parse_config import parse


def valid_path(path: str):
    return path is not None and not path.count('/') and path.isalnum()


def with_path(path: str):
    return path if valid_path(path.strip('/')) else None


def application(environ, start_response):
    path = environ['PATH_INFO']

    start_response('303 See Other', [('Location', environ['PATH_INFO'])])
    return []
