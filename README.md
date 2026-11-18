# kunfoo.org

A static website generated with [Pelican](https://getpelican.com/).

Dependencies are declared in `pyproject.toml` and resolved by
[uv](https://docs.astral.sh/uv/).

## Building the site
```
uv run pelican content
```

## Previewing
```
uv run pelican content --listen --autoreload
```

## Publishing
```
./update.sh
```

## Images
```
jpegoptim --max=85 --strip-all --all-progressive *.jpg
```
