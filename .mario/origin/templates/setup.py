{% block caution %}
# Block: caution
# {{ caution }}
{% endblock %}

{% block data_files %}
# Block: data_files
import os
data_files = {{ data_files }}
if data_files:
    try:
        if os.geteuid() != 0:
            data_files.clear()
    except Exception:
        pass
{% endblock %}

{% block long_description %}
# Block: long_description
from glob import iglob
long_description = '{{ description }}'
for filepath in iglob('README.*'):
    with open(filepath) as file:
        long_description = file.read()
    break     
{% endblock %}

{% block packages %}
# Block: packages
from setuptools import find_packages
packages = find_packages(os.path.dirname(__file__) or '.', exclude=['tests*'])
{% endblock %}

{% block setup %}
# Block: setup
from setuptools import setup
setup(
    author='{{ author }}',
    author_email='{{ author_email }}',
    classifiers={{ classifiers }},       
    description='{{ description }}',
    data_files=data_files,
    download_url='https://github.com/{{ github_user }}/{{ name }}/tarball/{{ version }}',
    entry_points={{ entry_points }},
    license='{{ license }}',
    long_description=long_description,
    maintainer='{{ maintainer }}',
    maintainer_email='{{ maintainer_email }}',
    name='{{ pypi_name }}',
    include_package_data=True,
    install_requires={{ install_requires }}, 
    packages=packages,
    platforms={{ platforms }},
    url='https://github.com/{{ github_user }}/{{ name }}',
    tests_require={{ tests_require }},
    test_suite='{{ test_suite }}',
    version='{{ version }}')
{% endblock %}
