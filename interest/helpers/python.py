import os


@property
def python(self):
    try:
        venv = os.environ['VIRTUAL_ENV']
        return os.path.join(venv, 'bin', 'python3')
    except KeyError:
        return 'python3'
