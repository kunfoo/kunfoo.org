#!/bin/sh

# jhead -purejpg docs/assets/*/*.jpg

# publishconf.py sets the absolute SITEURL and enables the Atom feeds.
uv run pelican content -s publishconf.py

# --delete keeps the server from accumulating pages that are no longer
# generated. /dl/ holds uploads that are not part of the build, and the
# exclusion protects it from being deleted along with them.
# -t preserves mtimes so unchanged images are not re-sent on every run; -O
# skips directory times, which the web root does not permit us to set.
rsync -rtvO --delete --exclude '/dl/' output/ kunfoo.org:/var/www/kunfoo.org/
