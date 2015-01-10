{% block caution %}
.. Block: caution

.. {{ caution }}
{% endblock %}

{% block description %}
.. Block: description

{{ name|capitalize }}
=====================
{{ description }}
{% endblock %}

{% block badges %}
.. Block: badges

.. image:: http://img.shields.io/badge/code-GitHub-brightgreen.svg
     :target: https://github.com/{{ github_user }}/{{ name }}
     :alt: code
.. image:: http://img.shields.io/travis/{{ github_user }}/{{ name }}/master.svg
     :target: https://travis-ci.org/{{ github_user }}/{{ name }} 
     :alt: build
.. image:: http://img.shields.io/coveralls/{{ github_user }}/{{ name }}/master.svg 
     :target: https://coveralls.io/r/{{ github_user }}/{{ name }}  
     :alt: coverage
.. image:: http://img.shields.io/badge/docs-latest-brightgreen.svg
     :target: http://{{ rtd_name }}.readthedocs.org
     :alt: docs     
.. image:: http://img.shields.io/pypi/v/{{ pypi_name }}.svg
     :target: https://pypi.python.org/pypi?:action=display&name={{ pypi_name }}
     :alt: pypi
{% endblock %}

{% block application %}
.. Block: application

Application
-----------
Package is under active development and is not ready for production use.
Backward-compatibility between minor releases (0.x.0), documentation and 
changelog are not guaranteed to be present before stable versions (>=1.0.0).
{% endblock %}

{% block requirements %}
.. Block: requirements

Requirements
------------
- Platforms

  {% for platform in platforms %}
  - {{ platform }}
  {% endfor %}
- Interpreters

  {% for interpreter in interpreters %}
  - Python {{ interpreter }}
  {% endfor %}
{% endblock %}

{% block installation %}
.. Block: installation

Installation
------------
- pip install {{ pypi_name }}
{% endblock %}

{% block contribution %}
.. Block: contribution

Contribution
------------
- Authors

  - {{ author }} <{{ author_email }}>
- Maintainers

  - {{ maintainer }} <{{ maintainer_email }}>
{% endblock %}

{% block changelog %}
.. Block: changelog

Changelog
---------
- no entries yet
{% endblock %}

{% block license %}
.. Block: license

License
-------
**{{ license }}**

{{ copyright }}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
{% endblock %}
