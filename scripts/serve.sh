#!/usr/bin/env bash
# Local Jekyll preview for ouha0.github.io
#
# Serves the site with drafts at http://127.0.0.1:4000
#
# Why the split config:
#   minimal-mistakes-jekyll is not on the GitHub Pages theme whitelist,
#   so the `theme:` line cannot live in _config.yml (it breaks the Pages
#   build). We keep it in _config.dev.yml instead — gitignored, local only.
#
# Why the PATH prefix:
#   `bundle install --path vendor/bundle` put the jekyll binary under
#   ~/bin, which isn't on PATH by default.

set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -f _config.dev.yml ]; then
  echo "error: _config.dev.yml is missing." >&2
  echo "Create it with a single line:" >&2
  echo '  theme: "minimal-mistakes-jekyll"' >&2
  exit 1
fi

PATH="$HOME/bin:$PATH" exec bundle exec jekyll serve \
  --drafts \
  --host 127.0.0.1 \
  --port 4000 \
  --config _config.yml,_config.dev.yml
