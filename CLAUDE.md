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

## Pseudonymous site

The site is deliberately not tied to the owner's real name. When editing
`_config.yml`, page front matter, or drafts, don't re-introduce the
real name, location, avatar, or personal social links. Placeholders in
`_config.yml` (empty `author.name`, empty `author.location`, commented-out
GitHub URL) should stay that way unless explicitly asked to change.

Strictness is low — the repo being at `ouha0.github.io` and the git history
already link the site to a GitHub handle, and that's acceptable. The goal
is just not to put identifying content on the rendered pages.

## Sections

Four sections, each with its own listing page:

- `/` (home) — short intro + recent posts across all categories.
- `/reflections/` — longer pieces. Posts need `categories: reflections` in front matter.
- `/notes/` — short reference material. Posts need `categories: notes`.
- `/experiments/` — small work-in-progress things. Posts need `categories: experiments`.
- `/about/`, `/library/` — static pages.

Section pages use `layout: archive` and iterate `site.categories.<name>`. The
author-profile sidebar is disabled globally via `author_profile: false` in
`_config.yml` defaults — don't re-add `author_profile: true` to page front matter.
