from os import path
import subprocess

MAKEFILE_NAMES = ['makefile', 'Makefile']

def Settings(**kwargs):
    if kwargs['language'] != 'cfamily':
        return {}

    # default flags
    flags = ['-Wall', '-Wextra', '-Werror']

    # get important variables from filepath
    dir_path, filename = path.split(kwargs['filename'])

    # get makefile path by stepping up until root
    makefile_path = None
    while makefile_path == None and dir_path != '/':
        for makefile_name in MAKEFILE_NAMES:
            tmp_path = path.join(dir_path, makefile_name)
            if path.isfile(tmp_path):
                makefile_path = tmp_path
                break
        dir_path = path.dirname(dir_path)

    # generate the flags from makefile output
    if makefile_path:
        makefile_path = path.dirname(makefile_path)
        ps = subprocess.Popen(('make', '-B', '-n', '-C', makefile_path), stdout=subprocess.PIPE)
        output = subprocess.check_output(('grep', '-P', filename), stdin=ps.stdout).decode('utf-8')
        ps.wait()

        flags = output.split(' ')[1:]

    return { 'flags': flags }
