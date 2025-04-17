from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, User
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def init_routes(app):
    app.register_blueprint(admin_bp)


@admin_bp.route('/users')
def list_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)


@admin_bp.route('/users/add', methods=['POST'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    if not username or not email or not password or not role:
        flash('Tous les champs sont obligatoires.', 'error')
        return redirect(url_for('admin.list_users'))

    if User.query.filter((User.username == username) | (User.email == email)).first():
        flash('Nom d\'utilisateur ou email déjà utilisé.', 'error')
        return redirect(url_for('admin.list_users'))

    password_hash = generate_password_hash(password)
    user = User(username=username, email=email, role=role, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    flash('Utilisateur ajouté avec succès.', 'success')
    return redirect(url_for('admin.list_users'))


@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Utilisateur supprimé.', 'success')
    else:
        flash('Utilisateur non trouvé.', 'error')
    return redirect(url_for('admin.list_users'))
