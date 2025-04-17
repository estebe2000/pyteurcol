"""
Application Flask pour la génération et l'évaluation d'exercices Python.

Cette application permet de générer des énoncés d'exercices Python, d'exécuter du code
et d'évaluer les solutions soumises par les élèves.
"""

import os
import sys

# Configuration de matplotlib pour le mode non-interactif
try:
    import matplotlib
    matplotlib.use('Agg')  # Mode non-interactif
except ImportError:
    pass  # Matplotlib n'est pas installé

from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User
from werkzeug.security import check_password_hash
from routes import main, data_editor, ged, notebook, defis
from routes import qcm_generator
from app.routes import admin_routes

# Configuration de l'application
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev_key_123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ged.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Initialisation SQLAlchemy avec l'application
db.init_app(app)

# Ajout de la commande CLI init-db
@app.cli.command("init-db")
def init_db_command():
    """Crée les tables de la base de données"""
    db.create_all()
    print("Base de données initialisée avec succès")

# Initialisation des routes
main.init_routes(app)
data_editor.init_routes(app)
ged.init_routes(app)
notebook.init_routes(app)
defis.init_routes(app)
qcm_generator.init_routes(app)

admin_routes.init_routes(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Connexion réussie.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Identifiants invalides.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Déconnecté.', 'success')
    return redirect(url_for('login'))


# Point d'entrée principal
if __name__ == '__main__':
    # Créer le répertoire de logs s'il n'existe pas
    os.makedirs('logs', exist_ok=True)
    app.run(debug=True)
