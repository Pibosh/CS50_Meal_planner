from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from passlib.hash import sha256_crypt as crypt
from tempfile import mkdtemp
from flask_jsglue import *
from helpers import *
import sqlite3

#adding JSGlue to ensure adding sripts to site

app = Flask(__name__)
JSGlue(app)

db = sqlite3.connect('data.db')

# ensure responses aren't cached
if app.config["DEBUG"]:
	@app.after_request
	def after_request(response):
		response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
		response.headers["Expires"] = 0
		response.headers["Pragma"] = "no-cache"
		return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
	flash('TODO', 'alert-info')
	return render_template('index.html')

@app.route('/check_recipes')
@login_required
def check_recipes():
	flash('TODO', 'alert-info')
	return render_template('check_recipes.html')

@app.route('/add_recipe')
@login_required
def add_recipe():
	flash('TODO', 'alert-info')
	return render_template('add_recipe.html')

@app.route('/generate_meals')
@login_required
def generate_meals():
	flash('TODO', 'alert-info')
	return render_template('generate_meals.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	"""Register user."""
	#clear any user currently logged in
	session.clear()

	#checking if user is using submiting form via POST method
	if request.method == "POST":
	#set variables from request forms
		username = request.form.get("username")
		password_1 = request.form.get("password_1")
		password_2 = request.form.get("password_2")
		email = request.form.get("email")

		#hash password
		hashed_passwd = crypt.hash(password_1)

		#user form are already validated by validate.js and _checkUser route
		db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashed_passwd)",
			   		username=username, hashed_passwd=hashed_passwd)

		#code for logging user in just after registration
		login = db.execute("SELECT * FROM users where username = :username", username=username)
		session["user_id"] = login[0]["id"]
		flash("Registered? Good!", 'alert-success')

	else:
		return render_template("register.html")

@app.route('/login')
def login():
	flash('TODO', 'alert-info')
	return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
	"""Log user out."""
	# forget any user_id
	session.clear()

	# redirect user to login form
	return redirect(url_for("login"))

@app.route('/_checkUser')
def _checkUser():
	"""TODO"""

@app.route('/_checkEmail')
def _checkEmail():
	"""TODO"""
