from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error404.html', error_name="404 - The Page can't be found"), 404


@app.errorhandler(500)
def not_found_error(error):
    db.session.rollback()
    return render_template('error500.html', error_name="500 - Internal server error"), 500
