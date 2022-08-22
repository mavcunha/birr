from parse_config import parse

def valid_key(path):
    # will consider a valid path if has no slashes and is not None
    return path is not None and not path.count('/') and path.isalnum()

def clean_path(path):
    return path.strip('/') if path else None

def application(environ, start_response):
    path = clean_path(environ.get('PATH_INFO', 'default'))
    shorts = parse('shorturls.cfg')

    # if not path was given, let's fallback to 'default'
    # as key. If that is not present, than 404
    if not path:
        path = 'default'

    if valid_key(path) and path in shorts:
        start_response('303 See Other', [('Location', shorts[path])])
    else:
        start_response('404 Not Found', [('Content-type', 'text/plain')])

    return []
