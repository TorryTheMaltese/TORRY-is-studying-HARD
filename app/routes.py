from app import app
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, login_required, current_user, logout_user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signOut')
def sign_out():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signIn', methods=['GET', 'POST'])
def sign_in():
    return render_template('signIn.html')


@app.route('/signUp', methods=['GET', 'POST'])
def sign_up():
    return render_template('signUp.html')


@app.route('/user/<user_id>')
@login_required
def user(user_id):
    return render_template('user.html')