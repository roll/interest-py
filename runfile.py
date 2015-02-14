import os
import mario
from pathlib import Path
mario.activate(basedir=os.path.dirname(__file__))
from mario.origin import ProjectModule  # @UnresolvedImport


class ProjectModule(ProjectModule):

    # Public

    author = 'roll'
    author_email = 'roll@respect31.com'
    copyright = '2015, Inventive Ninja'
    description = 'Interest is a event-driven web framework on top of aiohttp/asyncio.'
    development_requires = [
        'runfile', 'mario', 'sphinx', 'sphinx-settings', 'sphinx-rtd-theme']
    github_user = 'inventive-ninja'
    install_requires = ['aiohttp>=0.14']
    interpreters = ['3.4']
    license = 'MIT License'
    name = 'interest'
    platforms = ['Unix']
    pypi_password_secure = 'eN3OOqIkf4QsVDzJnCoXGRUOtUwqBBu+nu8V52QBzBdlSJ+Vs8FNFgfkZ1RBK0f1O10OHNzKxtM7l9oKx17DD/vsxT3FyP/VmFZs2GLkmXIT1652o42vuiSUuY736KboXOU6NzoQjjK4uKXn89vAoWY9R/CFUpLkgtw24LwKSiw='
    tests_require = ['nose', 'coverage']
    test_suite = 'nose.collector'
    version = '0.4.0'

    @property
    def examples(self):
        examples = {}
        directory = Path('demo')
        for path in directory.iterdir():
            if path.suffix == '.py':
                with path.open() as file:
                    examples[path.stem] = file.read()
        return examples
