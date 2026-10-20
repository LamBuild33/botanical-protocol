#!/usr/bin/env bash
# Rebuilds index.html (regular) and large-text.html from src/protocol.html.
# Needs Python 3, Node and Playwright (for the prerender step).
set -e
cd "$(dirname "$0")/.."
NODE_PATH=$(npm root -g) node scripts/prerender.js
python3 scripts/build_pages.py
sed -i 's|<title>Botanical Protocol</title>|<title>Botanical Protocol Tabs</title>|' build/tabs.html
# Large-text version = tabs version + extra CSS
python3 - <<'PY'
s=open('build/tabs.html').read()
css=open('src/large-text.css').read()
s=s.replace('<title>Botanical Protocol Tabs</title>','<title>Botanical Protocol Large Text</title>',1)
s=s.replace('</style>','\n'+css+'\n</style>',1)
open('build/large.html','w').write(s)
PY
wrap() { # turn a page fragment into a full stand-alone HTML file
  { printf '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%%}[hidden]{display:none!important}</style>\n'
    sed -n '1,/<\/style>/p' "$1"; printf '</head>\n<body>\n'
    sed -n '/<\/style>/,$p' "$1" | tail -n +2; printf '\n</body>\n</html>\n'; } > "$2"
}
wrap build/tabs.html index.html
wrap build/large.html large-text.html
echo "Built index.html and large-text.html"
