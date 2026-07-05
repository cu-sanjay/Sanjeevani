from datetime import datetime

from app import db


class Medication(db.Model):
    __tablename__ = "medications"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(100), nullable=True)
    frequency = db.Column(db.String(100), nullable=True)
    time_of_day = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.String(300), nullable=True)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    logs = db.relationship(
        "ReminderLog", backref="medication", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "time_of_day": self.time_of_day,
            "notes": self.notes,
            "active": self.active,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
        }


class ReminderLog(db.Model):
    __tablename__ = "reminder_logs"

    id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(
        db.Integer, db.ForeignKey("medications.id"), nullable=False
    )
    status = db.Column(db.String(20), nullable=False, default="taken")
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "medication_id": self.medication_id,
            "status": self.status,
            "logged_at": self.logged_at.strftime("%Y-%m-%d %H:%M"),
        }


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
