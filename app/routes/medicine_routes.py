from flask import Blueprint, abort, jsonify, render_template, request

from app.services.medicine_search import get_catalog

medicine_bp = Blueprint("medicine", __name__)


@medicine_bp.route("/")
def index():
    query = request.args.get("q", "")
    catalog = get_catalog()
    results = catalog.search(query) if query else catalog.medicines[:24]
    return render_template("medicines.html", medicines=results, query=query)


@medicine_bp.route("/search")
def search():
    query = request.args.get("q", "")
    catalog = get_catalog()
    results = catalog.search(query)
    return jsonify({"results": results})


@medicine_bp.route("/<int:med_id>")
def detail(med_id):
    catalog = get_catalog()
    medicine = catalog.get_by_id(med_id)
    if not medicine:
        abort(404)
    return render_template("medicine_detail.html", medicine=medicine)
