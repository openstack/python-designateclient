# -*- coding: utf-8 -*-
#
# designateclient documentation build configuration file

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinxcontrib.apidoc',
    'openstackdocstheme',
    'cliff.sphinxext']

# openstackdocstheme options
openstackdocs_repo_name = 'openstack/python-designateclient'
openstackdocs_bug_project = 'python-designateclient'
openstackdocs_bug_tag = ''
html_theme = 'openstackdocs'

apidoc_module_dir = '../../designateclient'
apidoc_output_dir = 'reference/api'
apidoc_excluded_paths = [ 'tests/*', 'functionaltests/*' ]
apidoc_separate_modules = True

autodoc_exclude_modules = [
  'designateclient.tests.*',
  'designateclient.functionaltests.*']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
copyright = u'2012, Managed I.T. 2013-2014, Hewlett-Packard Development Company, L.P.'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'native'

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ['designateclient']


# -- Options for HTML output ---------------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'designateclientdoc'
