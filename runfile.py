import os
import mario
mario.activate(basedir=os.path.dirname(__file__))
from mario.origin import ProjectModule  # @UnresolvedImport


class ProjectModule(ProjectModule):

    # Public

    author = 'roll'
    author_email = 'roll@respect31.com'
    copyright = 'Copyright (c) 2014 Respect31 <post@respect31.com>'
    description = 'Interest is a REST framework on top of aiohttp (experimental).'
    development_requires = [
        'mario', 'runfile', 'sphinx', 'sphinx-settings', 'sphinx-rtd-theme']
    github_user = 'interest-hub'
    install_requires = ['sugarbowl', 'aiohttp']
    interpreters = ['3.4']
    license = 'MIT License'
    name = 'interest'
    platforms = ['Unix']
    pypi_password_secure = 'eN3OOqIkf4QsVDzJnCoXGRUOtUwqBBu+nu8V52QBzBdlSJ+Vs8FNFgfkZ1RBK0f1O10OHNzKxtM7l9oKx17DD/vsxT3FyP/VmFZs2GLkmXIT1652o42vuiSUuY736KboXOU6NzoQjjK4uKXn89vAoWY9R/CFUpLkgtw24LwKSiw='
    tests_require = ['nose', 'coverage']
    test_suite = 'nose.collector'
    version = '0.0.0'
