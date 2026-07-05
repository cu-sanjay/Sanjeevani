import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

HEADERS = {"User-Agent": "Sanjeevani-Health-App/1.0 (educational hackathon project)"}

CATEGORY_TAGS = {
    "hospital": 'node["amenity"="hospital"](around:{radius},{lat},{lon});way["amenity"="hospital"](around:{radius},{lat},{lon});',
    "clinic": 'node["amenity"="clinic"](around:{radius},{lat},{lon});way["amenity"="clinic"](around:{radius},{lat},{lon});',
    "pharmacy": 'node["amenity"="pharmacy"](around:{radius},{lat},{lon});way["amenity"="pharmacy"](around:{radius},{lat},{lon});',
    "doctor": 'node["amenity"="doctors"](around:{radius},{lat},{lon});way["amenity"="doctors"](around:{radius},{lat},{lon});',
}


def geocode_place(place_name):
    params = {"q": place_name, "format": "json", "limit": 1}
    response = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=10)
    response.raise_for_status()
    results = response.json()
    if not results:
        return None
    return {
        "lat": float(results[0]["lat"]),
        "lon": float(results[0]["lon"]),
        "display_name": results[0]["display_name"],
    }


def find_resources(lat, lon, categories, radius=5000):
    if not categories:
        categories = list(CATEGORY_TAGS.keys())

    clauses = ""
    for category in categories:
        template = CATEGORY_TAGS.get(category)
        if template:
            clauses += template.format(radius=radius, lat=lat, lon=lon)

    query = f"""
    [out:json][timeout:25];
    (
      {clauses}
    );
    out center 60;
    """

    response = requests.post(OVERPASS_URL, data={"data": query}, headers=HEADERS, timeout=30)
    response.raise_for_status()
    data = response.json()

    places = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        name = tags.get("name")
        if not name:
            continue

        if "lat" in element and "lon" in element:
            place_lat, place_lon = element["lat"], element["lon"]
        elif "center" in element:
            place_lat, place_lon = element["center"]["lat"], element["center"]["lon"]
        else:
            continue

        amenity = tags.get("amenity", "facility")
        address_parts = [
            tags.get("addr:housenumber", ""),
            tags.get("addr:street", ""),
            tags.get("addr:city", ""),
        ]
        address = " ".join(part for part in address_parts if part).strip()

        places.append(
            {
                "name": name,
                "category": amenity,
                "lat": place_lat,
                "lon": place_lon,
                "address": address or "Address not listed",
                "phone": tags.get("phone", tags.get("contact:phone", "")),
                "opening_hours": tags.get("opening_hours", ""),
                "maps_url": f"https://www.openstreetmap.org/?mlat={place_lat}&mlon={place_lon}#map=18/{place_lat}/{place_lon}",
            }
        )

    return places
