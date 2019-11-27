from parse_config import parse


def valid_key(path: str):
    # will consider a valid path if has no slashes and is not None
    return path is not None and not path.count('/') and path.isalnum()


def clean_path(path: str):
    return path.strip('/') if path else None


def application(environ, start_response):
    path = clean_path(environ.get('PATH_INFO', ''))
    shorts = parse('shorturls.cfg')

    if valid_key(path) and path in shorts:
        start_response('303 See Other', [('Location', shorts[path])])
    else:
        start_response('200 OK', [('Content-type', 'text/plain')])

    return []
