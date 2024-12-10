from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db
from .forms import UserForm

bp = Blueprint('main', __name__, template_folder='templates')

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'warning')
        else:
            user = User(name=name, email=email)
            db.session.add(user); db.session.commit()
            flash('User created', 'success')
            return redirect(url_for('main.index'))
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('index.html', users=users, form=form)

@bp.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user); db.session.commit()
    flash('User deleted', 'info')
    return redirect(url_for('main.index'))

@bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        db.session.commit()
        flash('Updated', 'success')
        return redirect(url_for('main.index'))
    return render_template('edit.html', form=form, user=user)