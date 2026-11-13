"""Turn the Wikidata executives CSV into LinkedIn's Connections.csv layout for a ScanAxe test import.

Usage: python to_connections.py <executives.csv> <Connections.csv>
Only rows with a LinkedIn profile id are written (the import needs an email or a profile URL). Email and
"Connected On" stay empty: these people are NOT the owner's connections, so the import must use a basis other
than "connected" (for example legitimate interest), and the strict compliance default blocks cold outreach.
"""
import csv
import sys


def main(src, dst):
    seen = set()
    with open(src, newline="", encoding="utf-8") as f, open(dst, "w", newline="", encoding="utf-8") as out:
        w = csv.writer(out)
        w.writerow(["First Name", "Last Name", "URL", "Email Address", "Company", "Position", "Connected On"])
        n = 0
        for r in csv.DictReader(f):
            lid = (r.get("linkedin") or "").strip()
            name = (r.get("person_name") or "").strip()
            if not lid or not name or (lid, r.get("company")) in seen:
                continue
            seen.add((lid, r.get("company")))
            first, _, last = name.partition(" ")
            w.writerow([first, last, f"https://www.linkedin.com/in/{lid}", "", r.get("company_name", ""), r.get("role", ""), ""])
            n += 1
    print(f"{n} people with a LinkedIn profile")


if __name__ == "__main__":
    main(*sys.argv[1:3])
