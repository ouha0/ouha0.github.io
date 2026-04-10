# Project notes for Claude

Jekyll site hosted on GitHub Pages at https://ouha0.github.io.

## Local preview

Run `./scripts/serve.sh` from the repo root. Site serves at http://127.0.0.1:4000
with drafts included.

## GitHub Pages gotcha

The `minimal-mistakes-jekyll` theme is **not** on the GitHub Pages theme
whitelist. Do not set `theme:` in `_config.yml` — it breaks the Pages build
with `MissingDependencyException`.

The repo vendors `_layouts/`, `_includes/`, and `_sass/` directly, so Pages
builds fine without the theme line.

For local development, the theme line lives in `_config.dev.yml` (gitignored).
Jekyll merges it on top of `_config.yml` via the `--config` flag in
`scripts/serve.sh`.

## Drafts

Drafts live in `_drafts/`. Jekyll excludes this directory from the default
build, so committing and pushing a draft does not publish it. Local preview
via `scripts/serve.sh` includes drafts because of the `--drafts` flag.
