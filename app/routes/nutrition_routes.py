from flask import Blueprint, abort, render_template

from app.services.nutrition import get_plan, list_conditions

nutrition_bp = Blueprint("nutrition", __name__)


@nutrition_bp.route("/")
def index():
    return render_template("nutrition.html", conditions=list_conditions())


@nutrition_bp.route("/<condition_id>")
def plan(condition_id):
    data = get_plan(condition_id)
    if not data:
        abort(404)
    return render_template("nutrition_plan.html", plan=data, conditions=list_conditions(), active_id=condition_id)
