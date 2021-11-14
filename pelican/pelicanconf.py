import os
from pelican.readers import MarkdownReader


INFINITE_PELICAN_VERSION = "0.1.0"

INFINITE_PELICAN_IMG = '/img/cin.png'
INFINITE_PELICAN_TITLE = 'Infinite Cincinnati'

INFINITE_PELICAN_TITLE_CLASS = 'cincinnati'


# Yes, this is supposed to be UI not URI...
SITEURL = os.environ.get('INFINITE_BASE_UI', '')

AUTHOR = u'Ch4zm of Hellmouth'

HERE = os.path.abspath(os.path.dirname(__file__))

SITENAME = INFINITE_PELICAN_TITLE

PATH = 'content'
THEME = 'infinite-cleveland-pelican-theme'

# Don't try to turn HTML files into pages
READERS = {
    'html': None,
    'md': MarkdownReader
}

# Static stuff
STATIC_PATHS = ['img', 'almanacs']


# --------------------
# Map template pages to their final file name

TEMPLATE_PAGES = {}

TEMPLATE_PAGES['index.html'] = 'index.html'

# --------------------
# Add custom routes

THEME_TEMPLATES_OVERRIDES = []
#THEME_TEMPLATES_OVERRIDES.append('foobar')
#TEMPLATE_PAGES['foobar/special.html'] = 'foobar/index.html'

# --------------------
# SHUT UP

ARCHIVES_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
DAY_SAVE_AS = ''
INDEX_SAVE_AS = ''
MONTH_ARCHIVE_SAVE_AS = ''
TAGS_SAVE_AS = ''
YEAR_ARCHIVE_SAVE_AS = ''


# ---------------------

# No feeds
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
DEFAULT_PAGINATION = False
TIMEZONE = 'America/Los_Angeles'

