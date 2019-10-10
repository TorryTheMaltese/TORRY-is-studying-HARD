from app import app, login, models
from flask import render_template, request, redirect, url_for, flash, abort, session
from flask_login import login_user, login_required, current_user, logout_user
from app.forms import SignInForm, SignUpForm, EditUserForm, UploadForm
from datetime import datetime
import dbHelper


@login.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/')
def index():
    return render_template('index.html')


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
        print(session['user_id'])
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
    posts = [
        {'author': user, 'body': 'Text post #1'},
        {'author': user, 'body': 'Text post #2'}
    ]

    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = EditUserForm()
    if form.validate_on_submit():
        current_user.user_email = form.user_email.data
        current_user.user_password = form.user_password.data
        current_user.user_name = form.user_name.data

        try:
            with dbHelper.get_session() as session:
                session.commit()

        except Exception as e:
            abort(500)

        flash('Your changes have been saved.')
        return redirect(url_for('user', user_email=current_user.user_email))

    form.user_email.data = current_user.user_email or ''
    form.user_name.data = current_user.user_name

    return render_template('edit_user.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm(request.form)
    if form.validate_on_submit():
        board = models.Board(board_title=form.board_title.data, board_image=form.board_image.data)
        try:
            with dbHelper.get_session() as session:
                session.add(board)
        except Exception as e:
            return render_template('index.html', error=str(e))
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.user_last_seen = datetime.utcnow()

        try:
            with dbHelper.get_session() as session:
                session.commit()

        except Exception as e:
            abort(500)
