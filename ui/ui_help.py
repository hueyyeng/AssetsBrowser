import tempfile


def help_repath(path):
    f = tempfile.NamedTemporaryFile(suffix='.html', delete=False)

    with f as temp:
        data = open(path, 'r')
        text = data.read()
        text = text.replace('../../', '')
        temp.write(text)
        # temp.seek(0)
        # repath = temp.read()
        # print repath

    h = f.name
    return h.replace('\\', '/')
