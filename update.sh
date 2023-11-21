#!/bin/sh

jhead -purejpg docs/assets/*/*.jpg
. venv/bin/activate
mkdocs build
rsync -vr site/ kunfoo.org:/var/www/kunfoo.org/
