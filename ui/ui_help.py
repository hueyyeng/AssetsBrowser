# -*- coding: utf-8 -*-
import tempfile
import platform


def repath(path):
    file = tempfile.NamedTemporaryFile(suffix='.html', delete=False)

    with file as temp:
        data = open(path, 'r')
        text = data.read()
        # text = text.replace('../../', '')  # Python2.7
        text = text.replace('../../', '').encode('utf-8')
        temp.write(text)
        help_path = file.name

    system = platform.system()

    if system == 'Windows':
        help_path.replace('\\', '/')

    return help_path
