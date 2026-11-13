"""Extract businesses from an OpenStreetMap .pbf into the tab-separated layout of the Overpass export.

Usage: python osm_extract.py <file.osm.pbf> <ISO> <out.tsv>
Only kind tags, names and websites are written: no phones, emails, addresses or coordinates.
Data © OpenStreetMap contributors, ODbL 1.0.
"""
import re
import sys

import osmium

COLS = ["brand:wikidata", "brand", "operator", "name", "website", "contact:website", "brand:website",
        "amenity", "shop", "leisure", "tourism", "office", "healthcare", "craft", "industrial"]
AMENITY = re.compile(r"^(restaurant|fast_food|cafe|food_court|ice_cream|bar|pub|clinic|hospital|"
                     r"pharmacy|school|college|university|kindergarten|bank|car_rental|fuel)$")
LEISURE = re.compile(r"^(fitness_centre|sports_centre|sports_hall|stadium|water_park|ice_rink|bowling_alley|"
                     r"amusement_arcade|trampoline_park)$")
TOURISM = re.compile(r"^(hotel|motel|resort|guest_house|hostel|apartment|theme_park)$")
NAMED = ("brand", "operator", "website", "contact:website")
WEB = ("website", "contact:website", "brand")


PERSON = re.compile(r"^\s*(dr\.?|د\.|دكتور|prof\.?)\s", re.I)


def keep(t) -> bool:
    if PERSON.match(t.get("name") or ""):
        return False
    has = lambda keys: any(t.get(k) for k in keys)
    if t.get("amenity") and AMENITY.match(t.get("amenity")):
        return has(NAMED)
    if t.get("shop"):
        return has(NAMED)
    if t.get("leisure") and LEISURE.match(t.get("leisure")):
        return has(NAMED)
    if t.get("tourism") and TOURISM.match(t.get("tourism")):
        return has(NAMED)
    if t.get("office") or t.get("industrial"):
        return has(WEB)
    return False


def clean(v) -> str:
    return re.sub(r"[\t\r\n]+", " ", v or "").strip()[:300]


class Handler(osmium.SimpleHandler):
    def __init__(self, out):
        super().__init__()
        self.out, self.count = out, 0

    def write(self, kind, tags):
        if keep(tags):
            self.out.write("\t".join([kind, ""] + [clean(tags.get(c)) for c in COLS]) + "\n")
            self.count += 1

    def node(self, n):
        if len(n.tags):
            self.write("node", n.tags)

    def way(self, w):
        if len(w.tags):
            self.write("way", w.tags)

    def relation(self, r):
        if len(r.tags):
            self.write("relation", r.tags)


def main(pbf, iso, path):
    with open(path, "w", encoding="utf-8") as out:
        out.write("\t".join(["@type", "ISO3166-1"] + COLS) + "\n")
        out.write("\t".join(["area", iso] + [""] * len(COLS)) + "\n")
        h = Handler(out)
        h.apply_file(pbf)
    print(f"{iso}: {h.count} places")


if __name__ == "__main__":
    main(*sys.argv[1:4])
