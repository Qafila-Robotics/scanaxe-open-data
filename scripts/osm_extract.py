"""Extract businesses from an OpenStreetMap .pbf into the tab-separated layout of the Overpass export.

Usage: python osm_extract.py <file.osm.pbf> <ISO|AUTO> <out.tsv>
With AUTO (a file that covers several countries, such as Geofabrik's GCC states), each place's country is
taken from its location with the offline reverse_geocoder package; the location itself is never written.
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
    def __init__(self, auto):
        super().__init__()
        self.auto, self.rows, self.points = auto, [], []

    def write(self, kind, tags, point):
        if keep(tags) and (point or not self.auto):
            self.rows.append("\t".join([kind, "%s"] + [clean(tags.get(c)) for c in COLS]))
            self.points.append(point)

    def node(self, n):
        if len(n.tags):
            self.write("node", n.tags, (n.location.lat, n.location.lon) if self.auto and n.location.valid() else None)

    def way(self, w):
        if len(w.tags):
            point = None
            if self.auto:
                for nd in w.nodes:
                    if nd.location.valid():
                        point = (nd.location.lat, nd.location.lon)
                        break
            self.write("way", w.tags, point)

    def relation(self, r):
        if len(r.tags) and not self.auto:
            self.write("relation", r.tags, None)


def main(pbf, iso, path):
    auto = iso == "AUTO"
    h = Handler(auto)
    h.apply_file(pbf, locations=auto)
    groups = {}
    if auto:
        import reverse_geocoder
        found = reverse_geocoder.search(h.points, mode=1) if h.points else []
        for row, hit in zip(h.rows, found):
            groups.setdefault(hit["cc"], []).append(row)
    else:
        groups[iso] = h.rows
    with open(path, "w", encoding="utf-8") as out:
        out.write("\t".join(["@type", "ISO3166-1"] + COLS) + "\n")
        for cc, rows in sorted(groups.items()):
            out.write("\t".join(["area", cc] + [""] * len(COLS)) + "\n")
            for row in rows:
                out.write(row.replace("%s", "", 1) + "\n")
            print(f"{cc}: {len(rows)} places")


if __name__ == "__main__":
    main(*sys.argv[1:4])
