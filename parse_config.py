
def lines(file_name):
    try:
        with open(file_name) as file:
            for line in file:
                if not ignore(line):
                    yield line.strip()
    except OSError:
        raise ValueError('File {file} not found'.format(file=file_name))


def ignore(line: str):
    ls = line.strip()
    return (not ls
            or ls.startswith('#')
            or len(ls.split()) <= 2)


def break_line(line):
    tokens = line.split()
    return tokens[-1], tokens[:-1]


def list_to_keys(value, keys: list):
    return {key: value for key in keys}


def shortcut(line):
    return {key: url for key, url in list_to_keys(*break_line(line)).items()}


def parse(file_name='shorturls.cfg'):
    shorts = {}
    for line in lines(file_name):
        shorts.update(shortcut(line))
    return shorts
