# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Site Architecture

A static site generated with Pelican, using a custom theme in `theme/kunfoo/`.

- **Content**: blog posts and pages in `content/` as Markdown
- **Blog posts**: one directory per date, `content/YYYY-MM-DD/`, with images alongside
- **Pages**: `content/pages/`
- **Theme**: `theme/kunfoo/` — templates, CSS, one small script
- **Output**: `output/` (gitignored, regenerated)
- **Configuration**: `pelicanconf.py`; `publishconf.py` adds production-only settings

Templates not present in `theme/kunfoo/templates/` fall through to Pelican's
bundled `simple` theme. Anything inherited from `simple` is unstyled by this
theme's CSS, so prefer adding an override here over leaving the fallback in place.

### Content Structure

```
Title: Post Title
Category: Blog
Date: YYYY-MM-DD
Tags: tag1, tag2
Slug: url-slug
Lang: de/en
```

`DEFAULT_LANG` is `de`. Two files sharing a title/slug with different `Lang:`
values become one post plus a translation: the one matching `DEFAULT_LANG` is
canonical, the other gets the `-{lang}` URL suffix from `ARTICLE_LANG_URL`.
Translations do not appear separately in the archive; they are reachable from
the `language` row on the canonical post.

## Development Commands

Dependencies are declared in `pyproject.toml` and resolved by `uv`. There is no
virtualenv to activate and no `make` or `invoke` on this machine.

```bash
# Generate the site into output/
uv run pelican content

# Regenerate on change and serve at http://localhost:8000
uv run pelican content --listen --autoreload

# Serve an existing build without regenerating
python3 -m http.server 8000 --bind 127.0.0.1 --directory output

# Production build: absolute SITEURL, feeds enabled
uv run pelican content -s publishconf.py
```

### Publishing

```bash
./update.sh              # production build, then rsync to kunfoo.org
```

`update.sh` builds with `publishconf.py` — absolute `SITEURL`, Atom feeds —
and rsyncs `output/` to `kunfoo.org:/var/www/kunfoo.org/`. Things to know:

- It runs `--delete`, so **anything not in `output/` is removed from the
  server**. Check `rsync -n` output before deploying after a change that moves
  or stops generating URLs; renaming a post or changing its date orphans the
  old path, and the next deploy will take it away.
- `/dl/` is protected by `--exclude '/dl/'`. It holds a 526MB upload that is
  not part of the build. Any other server-side content that Pelican does not
  generate needs its own exclusion or it will be deleted.
- `-O` is deliberate: the web root's mtime cannot be set by the deploying user,
  and without it rsync exits 23 on every run, which would hide real failures.

`Makefile` and `tasks.py` are Pelican's generated scaffolding and assume a
virtualenv that does not exist here. They are kept for reference only.
`invoke publish` is **not functional**: its rsync command interpolates
`{ssh_user}`, `{ssh_host}`, `{ssh_port}` and `{ssh_path}`, none of which are
defined in `CONFIG`. Use `./update.sh`.

### Content Management

```bash
./new_post.sh            # create a dated directory and open an editor
```

### Image Optimization

```bash
jpegoptim --max=85 --strip-all --all-progressive *.jpg
```

## Theme

### Layout: the ledger

Every list on the site is the same two-column grid — a label or date in the
first column, a title or value in the second — so the landing page, archive,
tag pages and article metadata all read as one aligned record.

That markup lives in **one** place, the `post_rows()` macro in
`templates/_rows.html`. Four templates previously held copies of it and drifted
apart; add callers rather than new copies.

The grid is `.rows` in `main.css` and collapses to a single column below 30rem,
where a two-column German headline stops fitting.

### Templates

| Template | Role |
|---|---|
| `base.html` | Shell: head, masthead, footer, scheme toggle. No navigation. |
| `landing.html` | Homepage. Wordmark, intro, 3 recent posts, contact. |
| `_rows.html` | `post_rows()` macro — the ledger list. |
| `archives.html` | The site's only full post list. |
| `index.html` | Paginated list; extended by `tag.html` and `category.html`. Not generated (see below) but still the parent template. |
| `article.html`, `page.html` | Single entries. Title is the `h1`; metadata uses `.rows`. |
| `tag.html`, `category.html` | Heading only; inherit the list from `index.html`. |
| `pagination.html` | "newer"/"older" rather than prev/next, for reverse-chronological lists. |

`base.html` exposes a `masthead` block: it renders a quiet link home by
default, and `landing.html` replaces it with the `h1` wordmark.

### Typography

System font stacks only (`--font-text`, `--font-data`). No webfont is loaded:
no extra request, no FOUT, no layout shift. Keep it that way unless a face is
self-hosted as woff2.

Body measure is `--measure` (42rem, roughly 78 characters). `text-wrap: balance`
is for headings only — it silently gives up past 6 lines in Chromium and costs
a binary search, so it must stay off body copy, which uses `pretty`.

### Colour scheme

`main.css` defines colour as light/dark pairs and resolves them with
`light-dark()`, falling back to `prefers-color-scheme` under
`@supports not (...)`. Two rules are load-bearing:

- `:root` **must** keep `color-scheme: light dark`. It is what makes the page
  follow the system preference when no override is stored.
- `theme.js` records an override by rewriting `<meta name="color-scheme">`, and
  CSS maps that back onto the property with
  `:root:has(> head > meta[name="color-scheme"][content="dark"])`. Without that
  mapping the meta is only a presentational hint and the `:root` declaration
  outranks it, so the toggle silently does nothing.

`theme/kunfoo/static/js/theme.js` is the only script on the site. It stores an
override only when it diverges from the OS, and deletes it when the user
toggles back to match — so an OS on a day/night schedule can still be followed.
A stored value is kept even once the OS catches up to it. The footer button
ships with the `hidden` attribute and the script removes it, so with JS off
there is no dead control and the page still follows the system preference.

A small inline script in `base.html` applies the stored value before first
paint. It must stay parser-blocking (no `defer`, no `type=module`) and sit
immediately after the meta, or dark mode flashes white on load.

`rdark.css` is the Pygments theme; code blocks stay dark in both page themes
via `color-scheme: dark`. `main.css` overrides only its base text colour.

## Conventions and deliberate omissions

- **No navigation.** Removed on purpose; the landing page links what it links.
- **No author bylines or author pages.** One author. `AUTHOR_SAVE_AS`,
  `AUTHOR_URL` and `AUTHORS_SAVE_AS` are `''`.
- **No paginated blog index.** `INDEX_SAVE_AS = ''`; `/archives.html` is the
  post list. `/blog/YYYY/MM/DD/slug/` post URLs are unaffected.
- **`content/pages/about.md` is the homepage** via `save_as: index.html` plus
  `Template: landing`. It holds the intro prose only.
- **Contact details are config, not content**: the `CONTACT` tuple in
  `pelicanconf.py`, as `(label, text, url)`. A `url` of `None` renders unlinked.
  `pubkey.gpg` reaches the output through `STATIC_PATHS` and
  `EXTRA_PATH_METADATA` — it used to depend on an `{attach}` reference in
  `about.md`, which no longer exists.
- **`content/pages/kultur` is built but unlinked**, by request. `fahrrad` is
  linked from the intro prose.
- Other settings worth knowing: `LANDING_POST_COUNT` (recent posts on the
  homepage), `LANG_NAMES` (language names for the translation switcher).

## Known follow-ups

- Wide markdown tables can still push the page sideways. The fix needs a scroll
  container wrapping `<table>`, which Markdown cannot emit without a small
  extension. Applying `display: block` to the table instead would break it for
  screen readers.
- Post images carry no intrinsic dimensions, so they reflow as they load.
  Fixing this means width/height attributes or `aspect-ratio` per image.

## Browser support

Target modern evergreen browsers across engines, not Chrome alone. Prefer
platform HTML/CSS over libraries and over script. Features below Baseline
Widely available are acceptable when they degrade silently with no script, as
cross-document `@view-transition` would; do not add polyfills or client-side
scripts to reach them.
