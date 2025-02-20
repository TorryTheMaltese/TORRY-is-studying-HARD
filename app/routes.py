from app import app, login, models, db
from flask import render_template, request, redirect, url_for, flash, abort, session
from flask_login import login_user, login_required, current_user, logout_user
from app.forms import SignInForm, SignUpForm, EditUserForm, EditPasswordForm, UploadForm
from datetime import datetime
from werkzeug.utils import secure_filename
import dbHelper
import os


@login.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/', methods=['GET', 'POST'])
def index():
    posts = models.Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if request.method == 'POST':
        post_image = form.post_image.data
        if not post_image:
            flash('No Chosen')
            return redirect(url_for('index'))
        post_image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(post_image.filename)))
        post = models.Post(post_title=form.post_title.data, post_image=secure_filename(post_image.filename))
        post.author = current_user
        try:
            with dbHelper.get_session() as session:
                session.add(post)
        except Exception as e:
            return render_template('index.html', error=str(e))
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/delete?<post_id>', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = models.Post.query.filter_by(id=post_id).first()
    db.session.query(models.Post).filter(models.Post.id==post.id).delete()
    db.session.commit()
    return redirect(url_for('user'))


@app.route('/signOut')
def sign_out():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signIn', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignInForm(request.form)

    if form.validate_on_submit():
        user = models.User.query.filter_by(user_email=form.user_email.data).first()
        if not user or not user.check_user_pw(form.user_password.data):
            flash('Invalid User ID or Password.')
            return redirect(url_for('sign_in'))
        login_user(user, remember=form.user_remember_me.data)
        return redirect(url_for('index'))

    return render_template('signIn.html', form=form)


@app.route('/signUp', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm(request.form)
    if form.validate_on_submit():
        user = models.User(user_email=form.user_email.data,
                           user_pw=form.user_password.data,
                           user_name=form.user_name.data)
        try:
            with dbHelper.get_session() as session:
                session.add(user)
        except Exception as e:
            return render_template('signUp.html', error=str(e))
        return redirect(url_for('index'))
    return render_template('signUp.html', form=form)


@app.route('/user')
@login_required
def user():
    user = models.User.query.filter_by(id=session['user_id']).first_or_404()
    posts = models.Post.query.filter_by(user_id=session['user_id'])
    return render_template('user.html', user=user, posts=posts)


@app.route('/editUser', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = EditUserForm()
    if form.validate_on_submit():
        current_user.user_email = form.user_email.data
        current_user.user_name = form.user_name.data

        try:
            with dbHelper.get_session() as session:
                session.commit()

        except Exception as e:
            abort(500)

        flash('Your changes have been saved.')
        return redirect(url_for('user'))

    form.user_email.data = current_user.user_email or ''
    form.user_name.data = current_user.user_name

    return render_template('editUser.html', form=form)


@app.route('/editPassword', methods=['GET', 'POST'])
@login_required
def edit_password():
    form = EditPasswordForm()
    if form.validate_on_submit():
        current_user.set_user_pw(form.user_new_password.data)

        try:
            with dbHelper.get_session() as session:
                session.commit()

        except Exception as e:
            abort(500)

        flash('Your changes have been saved.')
        return redirect(url_for('user'))

    form.user_password.data = current_user.user_pw or ''

    return render_template('editPassword.html', form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.user_last_seen = datetime.utcnow()

        try:
            with dbHelper.get_session() as session:
                session.commit()

        except Exception as e:
            abort(500)
