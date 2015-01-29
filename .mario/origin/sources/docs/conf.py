import os
import sphinx
import sphinx_rtd_theme
from sphinx_settings import Settings
project = 'name'  # REPLACE: project = '{{ name }}'
version = '0.0.0'  # REPLACE: version = '{{ version }}'


class Settings(Settings):

    # Documentation:
    # http://sphinx-doc.org/config.html

    # General

    extensions = ['sphinx.ext.autodoc']
    master_doc = 'index'
    pygments_style = 'sphinx'

    # Project

    project = project
    version = version

    # HTML

    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    html_show_copyright = False

    # Autodoc

    autodoc_member_order = 'bysource'
    autodoc_default_flags = ['members', 'special-members', 'private-members']
    autodoc_skip_members = ['__weakref__']


locals().update(Settings())
