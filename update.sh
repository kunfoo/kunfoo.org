#!/bin/sh

# jhead -purejpg docs/assets/*/*.jpg
# . venv/bin/activate
uv run pelican content
rsync -vr output/ kunfoo.org:/var/www/kunfoo.org/
