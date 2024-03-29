import warnings
from sphinx_gallery.scrapers import matplotlib_scraper

warnings.filterwarnings("ignore", category=UserWarning)


class matplotlib_svg_scraper(object):

    def __repr__(self):
        return self.__class__.__name__

    def __call__(self, *args, **kwargs):
        return matplotlib_scraper(*args, dpi=150, bbox_inches='tight', **kwargs)


# -- Project information -----------------------------------------------------

project = 'milkviz'
copyright = '2022, Mr-Milk'
author = 'Mr-Milk'

# The full version, including alpha/beta/rc tags
release = '0.6.0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_gallery.gen_gallery',
    'numpydoc',
    'sphinx.ext.autosummary'
]

sphinx_gallery_conf = {
    'examples_dirs': '../examples',  # path to your example scripts
    'gallery_dirs': 'gallery_examples',  # path to where to save gallery generated output
    'image_scrapers': (matplotlib_svg_scraper(),),
    'image_srcset': ["2x"],
}

autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
