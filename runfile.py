import os
import mario
mario.activate(basedir=os.path.dirname(__file__))
from mario.origin import ProjectModule  # @UnresolvedImport


class ProjectModule(ProjectModule):

    # Public

    author = 'roll'
    author_email = 'roll@respect31.com'
    copyright = 'Copyright (c) 2014 Respect31 <post@respect31.com>'
    description = 'Interest is a REST framework on top aiohttp (experimental).'
    development_requires = [
        'mario', 'runfile', 'sphinx', 'sphinx-settings', 'sphinx-rtd-theme']
    github_user = 'interest-hub'
    install_requires = ['sugarbowl', 'aiohttp']
    interpreters = ['3.3', '3.4']
    license = 'MIT License'
    name = 'interest'
    platforms = ['Unix']
    pypi_password_secure = ''
    tests_require = ['nose', 'coverage']
    test_suite = 'nose.collector'
    version = '0.0.0'
