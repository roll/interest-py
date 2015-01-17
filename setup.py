# Block: caution
# TO MAKE CHANGES USE [meta] DIRECTORY.

# Block: data_files
import os
data_files = []
if data_files:
    try:
        if os.geteuid() != 0:
            data_files.clear()
    except Exception:
        pass

# Block: long_description
from glob import iglob
long_description = 'Interest is a REST framework on top of aiohttp/asyncio (experimental).'
for filepath in iglob('README.*'):
    with open(filepath) as file:
        long_description = file.read()
    break     

# Block: packages
from setuptools import find_packages
packages = find_packages(os.path.dirname(__file__) or '.', exclude=['tests*'])

# Block: setup
from setuptools import setup
setup(
    author='roll',
    author_email='roll@respect31.com',
    classifiers=[],       
    description='Interest is a REST framework on top of aiohttp/asyncio (experimental).',
    data_files=data_files,
    download_url='https://github.com/interest-hub/interest/tarball/0.0.0',
    entry_points={},
    license='MIT License',
    long_description=long_description,
    maintainer='roll',
    maintainer_email='roll@respect31.com',
    name='interest',
    include_package_data=True,
    install_requires=['sugarbowl', 'aiohttp==0.13.1'], 
    packages=packages,
    platforms=['Unix'],
    url='https://github.com/interest-hub/interest',
    tests_require=['nose', 'coverage'],
    test_suite='nose.collector',
    version='0.0.0')
