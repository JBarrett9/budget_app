from flask import Blueprint, url_for, flash, render_template, request, redirect
from flask_login import current_user, login_user, logout_user, login_required

from budgetapp import bcrypt, db
from budgetapp.models import User
from budgetapp.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, AddUserForm, \
    UpdateAccountForm
from budgetapp.users.utils import send_reset_email, send_user_invite

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        user.content_id = user.id
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login Failed', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/password_reset", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An Email has been sent', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/password_reset/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Token has expired', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password updated successfully', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route("/account_settings", methods=['GET', 'POST'])
@login_required
def account():
    update_account_form = UpdateAccountForm()
    add_user_form = AddUserForm()

    if update_account_form.validate_on_submit():
        current_user.name = update_account_form.name.data
        current_user.email = update_account_form.email.data
        current_user.password = update_account_form.password.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        update_account_form.name.data = current_user.name
        update_account_form.email.data = current_user.email
        update_account_form.password.data = current_user.password

    if add_user_form.validate_on_submit():
        user = current_user
        email = add_user_form.email.data
        send_user_invite(user, email)
        flash('An invite has been sent', 'info')
        return redirect(url_for('users.account'))
    return render_template('account_settings.html', title='Account Settings', form=update_account_form,
                           add_user_form=add_user_form)


@users.route("/add_user", methods=['GET', 'POST'])
def add_user_request():
    form = AddUserForm()
    if form.validate_on_submit():
        user = current_user
        email = form.email.data
        send_user_invite(user, email)
        flash('An invite has been sent', 'info')
        return redirect(url_for('users.account'))
    return render_template('add_user.html', title='Add User', form=form)


@users.route("/add_user/<token>", methods=['GET', 'POST'])
def add_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    user = User.verify_add_token(token)
    if not user:
        flash('Token has expired', 'warning')
        return redirect(url_for('users.login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                        password=hashed_password, content_id=user.content_id)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Add Account', form=form)
