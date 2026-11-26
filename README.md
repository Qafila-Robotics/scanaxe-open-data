# ScanAxe open data

Open company data for testing ScanAxe. The company files hold no phones, emails, addresses, coordinates or
people. `data/people/` is the one exception: the names and roles of living public executives (CEO, founder,
chair) of businesses, as published on Wikidata (CC0), for local tests only. They are not your connections:
import them with a basis other than `connected`; ScanAxe's strict compliance default blocks cold outreach.

| File | Source | Licence |
|---|---|---|
| `data/world/<CC>.tsv.gz` (`GCC` holds AE, SA, QA, KW, BH and OM) | OpenStreetMap extracts from Geofabrik | © OpenStreetMap contributors, [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/) |
| `data/new/<CC>.tsv.gz` | Places the latest run found that the run before it did not have (matched by `@id`; on the first run, places first mapped in the last 90 days) | © OpenStreetMap contributors, ODbL 1.0 |
| `data/new-companies/GB.csv.gz` | Active UK companies incorporated in the 45 days before the monthly Companies House snapshot (number, name, category, date, SIC codes, post town) | Companies House free company data product, Crown copyright; Companies House imposes no rules on reuse of the public register |
| `data/wikidata/world-companies.csv.gz` | Wikidata Query Service | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) |

Each OpenStreetMap row ends with `@id`, `@version` and `@timestamp` (the object's last edit, UTC). A newly mapped
place is not always a newly opened one: mapping can come later than the opening.

The OpenStreetMap files are a derived database under the ODbL. Keep the credit
"© OpenStreetMap contributors" with any copy, and share any changed version under the same licence.

## Excluded countries
Iran (IR) and Cuba (CU) are not published, for sanctions: they are left out of `countries.tsv`, the
Wikidata queries, and any multi-country extract (`scripts/osm_extract.py`, `EXCLUDED`).

## Refresh

Actions → **world** → Run workflow (optionally `only` with a few codes from `countries.tsv`). Each country's
OpenStreetMap extract is downloaded from Geofabrik and filtered by `scripts/osm_extract.py`; Wikidata is asked
one country at a time with pauses.

## Use in ScanAxe

```sh
cd infra/local
curl -L -o data/QA.tsv.gz https://raw.githubusercontent.com/Qafila-Robotics/scanaxe-open-data/main/data/world/GCC.tsv.gz
gunzip -f data/QA.tsv.gz
docker compose exec api php artisan companies:import /data/QA.tsv --format=osm --workspace=<name> --icp-only
```
