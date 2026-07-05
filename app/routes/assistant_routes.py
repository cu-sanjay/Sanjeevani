from flask import Blueprint, jsonify, render_template, request

from app import db
from app.models import ChatMessage
from app.services.assistant import ask_assistant

assistant_bp = Blueprint("assistant", __name__)


@assistant_bp.route("/")
def index():
    history = ChatMessage.query.order_by(ChatMessage.created_at.asc()).limit(50).all()
    return render_template("assistant.html", history=history)


@assistant_bp.route("/ask", methods=["POST"])
def ask():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Please type a question first."}), 400

    recent = ChatMessage.query.order_by(ChatMessage.created_at.asc()).limit(20).all()
    history = [{"role": m.role, "content": m.content} for m in recent]

    user_msg = ChatMessage(role="user", content=message)
    db.session.add(user_msg)
    db.session.commit()

    result = ask_assistant(message, history=history)

    assistant_msg = ChatMessage(role="assistant", content=result["reply"])
    db.session.add(assistant_msg)
    db.session.commit()

    return jsonify({"reply": result["reply"], "ok": result.get("ok", False)})


@assistant_bp.route("/clear", methods=["POST"])
def clear():
    ChatMessage.query.delete()
    db.session.commit()
    return jsonify({"ok": True})
