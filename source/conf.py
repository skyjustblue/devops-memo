# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sphinx_rtd_theme

project = 'devops-memo'
copyright = '2024, fredo'
author = 'fredo'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    'myst_parser',  # 支持markdown
]

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme_options = {
    # 'sticky_navigation': False,  # 导航栏会在页面滚动时固定在页面顶部
    'collapse_navigation': True,  # ‌导航栏会折叠成一个小的按钮，‌用户可以点击它来展开或收起
    'navigation_depth': 6,  # 控制导航侧边栏目录深度
    'includehidden': True,
    # 'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,  # 控制是否对外部链接应用特定的样式
}

# myst_heading_anchors = 2  # 隐式链接：markdown 内联链接的标题深度
suppress_warnings = ["myst.header"]
