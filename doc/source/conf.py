# -*- coding: utf-8 -*-
#
# designateclient documentation build configuration file

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'openstackdocstheme']

# openstackdocstheme options
repository_name = 'openstack/python-designateclient'
bug_project = 'python-designateclient'
bug_tag = ''
html_last_updated_fmt = '%Y-%m-%d %H:%M'
html_theme = 'openstackdocs'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'designateclient'
copyright = u'2012, Managed I.T. 2013-2014, Hewlett-Packard Development Company, L.P.'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
from designateclient.version import version_info as designateclient_version
version = designateclient_version.canonical_version_string()
# The full version, including alpha/beta/rc tags.
release = designateclient_version.version_string_with_vcs()

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ['designateclient']


# -- Options for HTML output ---------------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'designateclientdoc'
