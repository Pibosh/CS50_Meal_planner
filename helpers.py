from flask import redirect, render_template, request, session, url_for, jsonify
from functools import wraps
import sqlite3

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def check_database(element, entry):
    #connect to database
	conn = sqlite3.connect('data.db')
	db = conn.cursor()

    db.execute("SELECT * FROM users WHERE ? = ?", (element, entry))
    user_check = db.fetchall()

    if len(user_check) != 0:
        return True
    else:
        return False
