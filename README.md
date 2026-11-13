# ScanAxe open data

Open company data for testing ScanAxe in the Gulf and MENA. Nothing here is personal data. There are no
phones, emails, addresses, coordinates or people.

| File | Source | Licence |
|---|---|---|
| `data/osm/<CC>.tsv`, `data/osm-mena.tsv` | OpenStreetMap through the public Overpass API | © OpenStreetMap contributors, [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/) |
| `data/wikidata/companies.csv` | Wikidata Query Service | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) |

The OpenStreetMap files are a derived database under the ODbL. Keep the credit
"© OpenStreetMap contributors" with any copy, and share any changed version under the same licence.

## Refresh

Actions → **fetch** → Run workflow (optionally with a shorter country list). The workflow runs one
country at a time with a pause between them, as the public Overpass server asks. The queries are in
`queries/`.

## Use in ScanAxe

```sh
cd infra/local
curl -L -o data/osm-mena.tsv https://raw.githubusercontent.com/Qafila-Robotics/scanaxe-open-data/main/data/osm-mena.tsv
docker compose exec api php artisan companies:import /data/osm-mena.tsv --format=osm --workspace=<name> --icp-only
```
