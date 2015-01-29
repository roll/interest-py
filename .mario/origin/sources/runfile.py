import os
import mario
mario.activate(basedir=os.path.dirname(__file__))
from mario.origin import ProjectModule  # @UnresolvedImport


class ProjectModule(ProjectModule):

    # Public

    author = '{{ author }}'
    author_email = '{{ author_email }}'
    copyright = '{{ copyright }}'
    description = '{{ description }}'
    development_requires = [
        'runfile', 'mario', 'sphinx', 'sphinx-settings', 'sphinx-rtd-theme']
    license = '{{ license }}'
    name = '{{ name }}'
    interpreters = ['3.3', '3.4']
    license = 'MIT License'
    platforms = ['Unix']
    pypi_password_secure = '{{ pypi_password_secure }}'
    tests_require = ['nose', 'coverage']
    test_suite = 'nose.collector'
    version = '0.0.0.'
