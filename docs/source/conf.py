# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'The EUPP postprocessing benchmark dataset documentation'
copyright = '2022, GIE EUMETNET - PP module'
author = 'GIE EUMETNET - PP module'

# The full version, including alpha/beta/rc tags
release = 'v1.0'  # version of the dataset, not of climetlab plugin
version = release

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    #    'nbsphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosectionlabel',
    'sphinxcontrib.bibtex',
    'jupyter_sphinx',
]

templates_path = ['_templates']
exclude_patterns = []

bibtex_bibfiles = ['refs.bib']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = "images/logo-eumetnet.png"
html_theme_options = {
    # 'logo_only': True,
    # 'display_version': False,
}

# -- Extension configuration -------------------------------------------------
# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'python': ('https://docs.python.org/3', None),
                       'numpy': ('https://numpy.org/doc/stable/', None),
                       'scipy': ('https://docs.scipy.org/doc/scipy/', None),
                       'matplotlib': ('https://matplotlib.org/stable/', None),
                       'sparse': ('https://sparse.pydata.org/en/stable/', None),
                       'sympy': ('https://docs.sympy.org/latest/', None),
                       'ipython': ('https://ipython.readthedocs.io/en/stable/', None),
                       'ipywidgets': ('https://ipywidgets.readthedocs.io/en/latest/', None),
                       'xarray': ('https://docs.xarray.dev/en/stable/', None)}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# mathjax config

mathjax_path = r"https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/latest.js?config=TeX-MML-AM_CHTML"

# autosection label option

autosectionlabel_prefix_document = True
