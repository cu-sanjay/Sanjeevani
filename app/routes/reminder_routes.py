from datetime import datetime

from flask import Blueprint, jsonify, render_template, request

from app import db
from app.models import Medication, ReminderLog

reminder_bp = Blueprint("reminder", __name__)


@reminder_bp.route("/")
def index():
    medications = Medication.query.order_by(Medication.created_at.desc()).all()
    logs = (
        ReminderLog.query.order_by(ReminderLog.logged_at.desc()).limit(30).all()
    )
    return render_template("reminders.html", medications=medications, logs=logs)


@reminder_bp.route("/add", methods=["POST"])
def add():
    name = request.form.get("name", "").strip()
    if not name:
        return jsonify({"error": "Medicine name is required."}), 400

    medication = Medication(
        name=name,
        dosage=request.form.get("dosage", "").strip(),
        frequency=request.form.get("frequency", "").strip(),
        time_of_day=request.form.get("time_of_day", "").strip(),
        notes=request.form.get("notes", "").strip(),
    )
    db.session.add(medication)
    db.session.commit()
    return jsonify({"medication": medication.to_dict()})


@reminder_bp.route("/<int:medication_id>/delete", methods=["POST"])
def delete(medication_id):
    medication = Medication.query.get_or_404(medication_id)
    db.session.delete(medication)
    db.session.commit()
    return jsonify({"ok": True})


@reminder_bp.route("/<int:medication_id>/log", methods=["POST"])
def log(medication_id):
    medication = Medication.query.get_or_404(medication_id)
    payload = request.get_json(silent=True) or {}
    status = payload.get("status", "taken")

    entry = ReminderLog(medication_id=medication.id, status=status, logged_at=datetime.utcnow())
    db.session.add(entry)
    db.session.commit()
    return jsonify({"log": entry.to_dict()})
