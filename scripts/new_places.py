"""List the places in a new extract that the previous extract did not have (the "new place" signal).

Usage: python new_places.py <previous.tsv.gz|-> <current.tsv.gz> <out.tsv.gz> [days]
Places are matched by `@id`. When there is no previous file, or it has no `@id` column yet, a place counts as
new when it is at version 1 and was first mapped within the last `days` days (default 90). The output keeps the
current file's columns and country markers. Data © OpenStreetMap contributors, ODbL 1.0.
"""
import csv
import gzip
import sys
from datetime import datetime, timedelta, timezone

csv.field_size_limit(sys.maxsize)


def ids(path):
    if path == "-":
        return None
    with gzip.open(path, "rt", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if "@id" not in (reader.fieldnames or []):
            return None
        return {row["@id"] for row in reader if row["@id"]}


def is_new(row, known, cutoff):
    if known is not None:
        return row["@id"] not in known
    return row.get("@version") == "1" and row.get("@timestamp", "") >= cutoff


def main(previous, current, out, days="90"):
    known = ids(previous)
    cutoff = (datetime.now(timezone.utc) - timedelta(days=int(days))).strftime("%Y-%m-%dT%H:%M:%SZ")
    count = 0
    with gzip.open(current, "rt", encoding="utf-8") as f, gzip.open(out, "wt", encoding="utf-8") as w:
        reader = csv.DictReader(f, delimiter="\t")
        writer = csv.DictWriter(w, fieldnames=reader.fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in reader:
            if row["@type"] == "area":
                writer.writerow(row)
            elif row.get("@id") and is_new(row, known, cutoff):
                writer.writerow(row)
                count += 1
    print(f"{out}: {count} new places ({'by id' if known is not None else 'first mapped since ' + cutoff[:10]})")


if __name__ == "__main__":
    main(*sys.argv[1:5])
