// One country (__CC__ is replaced by the workflow). Businesses with a brand, operator or website:
// food and drink, shops, hotels, sports, offices, clinics and hospitals, education, banks and industry.
// One-person practices (doctors, dentists, crafts) are left out: their names are often a person's name.
// Only kind tags, names and websites are exported; no phones, emails, addresses or coordinates.
// Data © OpenStreetMap contributors, ODbL 1.0.
[out:csv(::type, "ISO3166-1", "brand:wikidata", brand, operator, name, website, "contact:website", "brand:website", amenity, shop, leisure, tourism, office, healthcare, craft, industrial)][timeout:1500][maxsize:2147483648];
area["ISO3166-1"="__CC__"][admin_level=2]->.country;
.country out tags;
(
  nwr(area.country)[amenity~"^(restaurant|fast_food|cafe|food_court|ice_cream|bar|pub|clinic|hospital|pharmacy|school|college|university|kindergarten|bank|car_rental|fuel)$"][~"^(brand|operator|website|contact:website)$"~"."];
  nwr(area.country)[shop][~"^(brand|operator|website|contact:website)$"~"."];
  nwr(area.country)[leisure~"^(fitness_centre|sports_centre|sports_hall|stadium|water_park|ice_rink|bowling_alley|amusement_arcade|trampoline_park)$"][~"^(brand|operator|website|contact:website)$"~"."];
  nwr(area.country)[tourism~"^(hotel|motel|resort|guest_house|hostel|apartment|theme_park)$"][~"^(brand|operator|website|contact:website)$"~"."];
  nwr(area.country)[office][~"^(website|contact:website|brand)$"~"."];
  nwr(area.country)[industrial][~"^(website|contact:website|brand)$"~"."];
);
out tags;
