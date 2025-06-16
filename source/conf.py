# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Training: RegCM-OASIS-SYMPHONIE on CALMIP"
html_title = "Training: RegCM-OASIS-SYMPHONIE on CALMIP"
copyright = "2025, Quentin Desmet"
author = "Quentin Desmet"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"

html_theme_options = {
    "show_navbar_depth": 1,
    "collapse_navbar": False,
    "use_edit_page_button": False,
    "use_repository_button": False,
    "use_issues_button": False,
    "use_download_button": True,
    "toc_title": "Page contents",

}

html_sidebars = {
    "**": ["search-button-field.html", "sbt-sidebar-nav.html"]
}

html_static_path = ['_static']

html_css_files = [
    'custom.css',
]
