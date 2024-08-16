AUTHOR = 'katze'
SITENAME = 'kunfooses'
# SITEURL = "https://kunfoo.org"

PATH = "content"

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'de'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_PAGINATION = 10

THEME = './theme/kunfoo'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
"""
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)
"""

# Social widget
"""
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)
"""

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

# AUTHOR_URL = ''
# AUTHOR_SAVE_AS = ''
