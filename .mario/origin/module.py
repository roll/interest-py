import os
import inspect
from run import Module
from mario import MarioModule


class ProjectModule(Module):

    # Public

    mario = MarioModule()

    author = '<author>'
    author_email = '<author_email>'
    caution = 'TO MAKE CHANGES USE [meta] DIRECTORY.'
    classifiers = []
    copyright = '<copyright>'
    data_files = []
    description = '<description>'
    development_requires = []
    entry_points = {}
    install_requires = []
    interpreters = []
    license = '<license>'
    name = '<name>'
    platforms = []
    pypi_password_secure = '<pypi_password_secure>'
    tests_require = []
    test_suite = '<test_suite>'
    version = '<version>'

    def __init__(self):
        self.__update_pythonpath()

    @property
    def github_user(self):
        return self.author

    @property
    def maintainer(self):
        return self.author

    @property
    def maintainer_email(self):
        return self.author_email

    @property
    def pypi_name(self):
        return self.name

    @property
    def pypi_user(self):
        return self.author

    @property
    def rtd_name(self):
        return self.name

    # Private

    def __update_pythonpath(self):
        os.environ['PYTHONPATH'] = ':'.join([
            os.environ.get('PYTHONPATH', ''),
            os.path.abspath(os.path.dirname(inspect.getfile(type(self))))])
