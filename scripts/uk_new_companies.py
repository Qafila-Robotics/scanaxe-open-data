"""New UK companies from the Companies House free company data product (monthly snapshot).

Usage: uk_new_companies.py <BasicCompanyData.csv> <out.csv.gz> <snapshot YYYY-MM-DD> [days]

Keeps active companies incorporated in the `days` (default 45) before the snapshot day. Columns: number, name,
category, incorporated_on, SIC codes and the post town. No street address, postcode, officer or person.
"""
import csv
import gzip
import sys
from datetime import date, datetime, timedelta

OUT = ["company_number", "name", "category", "incorporated_on", "sic_codes", "post_town"]


def row_of(r):
    get = lambda k: (r.get(k) or "").strip()
    if get("CompanyStatus") != "Active":
        return None
    try:
        born = datetime.strptime(get("IncorporationDate"), "%d/%m/%Y").date()
    except ValueError:
        return None
    sics = [get(f"SICCode.SicText_{i}").split(" - ")[0] for i in range(1, 5)]
    sics = [s for s in sics if s.isdigit()]
    return born, [get("CompanyNumber"), get("CompanyName"), get("CompanyCategory"), born.isoformat(),
                  " ".join(sics), get("RegAddress.PostTown").title()]


def main(src, out, snapshot, days=45):
    since = date.fromisoformat(snapshot) - timedelta(days=int(days))
    kept = 0
    with open(src, newline="", encoding="utf-8-sig", errors="replace") as f, gzip.open(out, "wt", encoding="utf-8", newline="") as o:
        reader = csv.DictReader(f)
        reader.fieldnames = [h.strip() for h in reader.fieldnames]
        writer = csv.writer(o)
        writer.writerow(OUT)
        for r in reader:
            hit = row_of(r)
            if hit and hit[0] >= since:
                writer.writerow(hit[1])
                kept += 1
    print(f"GB: {kept} new companies since {since}")


if __name__ == "__main__":
    main(*sys.argv[1:])
