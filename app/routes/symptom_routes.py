from flask import Blueprint, jsonify, render_template, request

from app.services.symptom_checker import get_checker

symptom_bp = Blueprint("symptom", __name__)


@symptom_bp.route("/")
def index():
    checker = get_checker()
    return render_template("symptom_checker.html", symptoms=checker.symptom_list())


@symptom_bp.route("/check", methods=["POST"])
def check():
    payload = request.get_json(silent=True) or {}
    symptoms = payload.get("symptoms", [])
    checker = get_checker()
    results = checker.check(symptoms)
    return jsonify({"results": results})
