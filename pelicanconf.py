import hashlib
import os

AUTHOR = 'katze'
SITENAME = 'kunfooses'
# SITEURL = "https://kunfoo.org"

PATH = "content"

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'de'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_PAGINATION = 10

THEME = './theme/kunfoo'

# Cache busting. The stylesheet and script URLs carry a digest of their own
# contents, so a deploy changes the URL and no browser can go on serving an
# old stylesheet against new markup. nginx sends no Cache-Control, which
# leaves caching to browser heuristics that Chrome and Firefox disagree on.
_STATIC_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'theme', 'kunfoo', 'static')
_VERSIONED_ASSETS = ('css/main.css', 'css/rdark.css', 'js/theme.js')


def _asset_version():
    digest = hashlib.sha256()
    for relative_path in _VERSIONED_ASSETS:
        try:
            with open(os.path.join(_STATIC_ROOT, relative_path), 'rb') as handle:
                digest.update(handle.read())
        except OSError:
            # Never fail a build over a cache hint.
            return 'dev'
    return digest.hexdigest()[:10]


ASSET_VERSION = _asset_version()

# No top navigation. The landing page links what it wants to link.
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = ()

# Language names for the translation switcher on translated posts.
LANG_NAMES = {'de': 'Deutsch', 'en': 'English'}

# How many recent posts the landing page lists.
LANDING_POST_COUNT = 3

# Contact rows for the landing page ledger: (label, text, url).
# url = None renders the text without a link.
CONTACT = (
    ('mail', 'katze_at_kunfoo_dot_org', None),
    ('fediverse', '@katze@dresden.network', 'https://dresden.network/@katze'),
    ('gpg', 'pubkey.gpg', 'pubkey.gpg'),
)

# pubkey.gpg used to reach the output only because about.md referenced it
# with {attach}. Copy it explicitly now that the contact block is template-side.
STATIC_PATHS = ['images', 'pages/pubkey.gpg']
EXTRA_PATH_METADATA = {'pages/pubkey.gpg': {'path': 'pubkey.gpg'}}


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

# The flat archive is the only post list; the paginated index duplicated it.
INDEX_SAVE_AS = ''

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
ARTICLE_LANG_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}-{lang}/'
ARTICLE_LANG_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}-{lang}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

# One author, so per-author listings are just a duplicate archive.
AUTHOR_SAVE_AS = ''
AUTHOR_URL = ''
AUTHORS_SAVE_AS = ''
