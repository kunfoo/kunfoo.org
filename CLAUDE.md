# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Site Architecture

This is a static website generated with Pelican, a Python-based static site generator. The site uses a custom theme located in `theme/kunfoo/`.

### Key Components

- **Content**: All blog posts and pages are in `content/` as Markdown files
- **Blog posts**: Organized by date in `content/YYYY-MM-DD/` directories
- **Pages**: Static pages in `content/pages/`
- **Theme**: Custom Pelican theme in `theme/kunfoo/`
- **Output**: Generated HTML files go to `output/`
- **Configuration**: Main config in `pelicanconf.py`, publish config in `publishconf.py`

### Content Structure

Blog posts follow a date-based directory structure (`content/YYYY-MM-DD/blog_post.md`) and use Pelican metadata:
```
Title: Post Title
Category: Blog
Date: YYYY-MM-DD
Tags: tag1, tag2
Slug: url-slug
Lang: de/en
```

## Development Commands

### Setup Environment
```bash
python3 -m venv venv
. venv/bin/activate
pip install 'pelican[markdown]'
```

### Build and Serve
```bash
# Generate site
make html
# or
pelican content

# Serve locally at http://localhost:8000
make serve
# or
invoke serve

# Build and serve together
invoke reserve

# Auto-regenerate on changes
make regenerate
# or
invoke regenerate

# Live reload with browser refresh
invoke livereload
```

### Publishing
```bash
# Build production version
make publish
# or
invoke publish
```

### Content Management
```bash
# Create new blog post (creates dated directory and opens editor)
./new_post.sh
```

### Image Optimization
```bash
# Optimize images for web
jpegoptim --max=85 --strip-all --all-progressive *.jpg
```

## File Organization

- Blog posts use date-based URLs: `/blog/YYYY/MM/DD/slug/`
- Pages use simple URLs: `/slug/`
- Images and assets are stored alongside their respective posts
- The `template.md` file serves as a template for new blog posts

## Development Workflow

1. Use `./new_post.sh` to create new blog posts
2. Write content in Markdown with Pelican metadata
3. Use `invoke livereload` for development with auto-refresh
4. Run `make html` to build the site
5. Use `make serve` to preview locally
6. Run `make publish` for production builds
