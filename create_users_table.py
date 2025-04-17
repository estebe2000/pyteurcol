from app import app  # suppose que l'app Flask est dans app.py ou app/__init__.py
from models import db, User

with app.app_context():
    db.create_all()
    print("Tables créées (y compris User si elle n'existait pas).")
