from flask import Blueprint, jsonify, render_template, request

from app.services.resource_finder import find_resources, geocode_place

resource_bp = Blueprint("resource", __name__)


@resource_bp.route("/")
def index():
    return render_template("resources.html")


@resource_bp.route("/search", methods=["POST"])
def search():
    payload = request.get_json(silent=True) or {}
    lat = payload.get("lat")
    lon = payload.get("lon")
    place_name = payload.get("place_name")
    categories = payload.get("categories") or ["hospital", "clinic", "pharmacy", "doctor"]

    try:
        if place_name and not (lat and lon):
            location = geocode_place(place_name)
            if not location:
                return jsonify({"error": "That location could not be found. Try a different city or area."}), 404
            lat, lon = location["lat"], location["lon"]

        if not lat or not lon:
            return jsonify({"error": "Location is required to search for nearby care."}), 400

        places = find_resources(float(lat), float(lon), categories)
        return jsonify({"results": places, "lat": lat, "lon": lon})
    except Exception:
        return jsonify({"error": "The resource search failed. Please try again in a moment."}), 502
