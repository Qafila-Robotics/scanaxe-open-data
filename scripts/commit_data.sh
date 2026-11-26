#!/bin/bash
# Usage: commit_data.sh <artifact dir>
# Commits a world run's files onto the latest main. Each attempt starts from origin/main, so a push race never
# leaves a rebase conflict on a binary file. Excluded countries (sanctions) are dropped here too.
set -euo pipefail
art=$1
git config user.name "scanaxe-data"; git config user.email "data@users.noreply.github.com"
for i in 1 2 3 4 5; do
  git fetch -q origin main && git reset -q --hard origin/main
  mkdir -p data/world data/wikidata data/new
  for f in "$art"/osm-*/*.tsv.gz; do
    [ -e "$f" ] || continue
    cc=$(basename "$f" .tsv.gz)
    case "$cc" in IR|CU) continue ;; esac
    prev=data/world/$cc.tsv.gz; [ -e "$prev" ] || prev=-
    python3 scripts/new_places.py "$prev" "$f" "data/new/$cc.tsv.gz" 90
    cp "$f" data/world/
  done
  if [ -e "$art/wikidata/companies.csv.gz" ]; then
    python3 - "$art/wikidata/companies.csv.gz" data/wikidata/world-companies.csv.gz <<'PY'
import csv, gzip, io, sys
rows = csv.reader(io.TextIOWrapper(gzip.open(sys.argv[1]), encoding="utf-8"))
head = next(rows); i = head.index("country")
with gzip.open(sys.argv[2], "wt", encoding="utf-8", newline="") as f:
    w = csv.writer(f); w.writerow(head); w.writerows(r for r in rows if r[i] not in ("IR", "CU"))
PY
  fi
  git add data
  git diff --cached --quiet && { echo "nothing new"; exit 0; }
  git commit -q -m "World data refresh $(date -u +%F)"
  git push -q origin HEAD:main && exit 0
  sleep 20
done
exit 1
