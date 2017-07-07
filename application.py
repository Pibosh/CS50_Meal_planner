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

#connecting to database and creating a cursor
conn = sqlite3.connect('data.db')
db = conn.cursor()
#turning foreign_keys on according to sqlite3 docs
db.execute("PRAGMA foreign_keys = ON")

#creating a tables - if it doesn't exist
#first - create table for user with id, username, password, email and verification
db.execute("CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER PRIMARY KEY \
			AUTOINCREMENT NOT NULL, 'username' TEXT NOT NULL, 'hash' TEXT \
			NOT NULL, 'email' TEXT NOT NULL, 'veryfied' BOOLEAN DEFAULT 0, \
			UNIQUE (username), UNIQUE (email) );")
#then - create table containing recipes
db.execute("CREATE TABLE IF NOT EXISTS 'recipe' ('recipe_id' INTEGER PRIMARY KEY \
			AUTOINCREMENT NOT NULL, 'user_id' INTEGER, \
			'title' VARCHAR(150) NOT NULL, 'prepare' \
			TEXT NOT NULL, 'meal_type' TEXT, \
			FOREIGN KEY (user_id) REFERENCES users(id), UNIQUE (title), \
			CHECK (meal_type IN ('breakfast', 'dinner', 'supper') ));")
#then - create table containing ingridients
db.execute("CREATE TABLE IF NOT EXISTS 'ingridients' ('ingridient_id' INTEGER PRIMARY \
			KEY AUTOINCREMENT NOT NULL, 'ingridient_name' VARCHAR(150), 'unit' \
			VARCHAR(5), UNIQUE (ingridient_name));")
#then - create table containing recipe_items - ingridients for particular recipe
db.execute("CREATE TABLE IF NOT EXISTS 'recipe_items' ('item_id' INTEGER PRIMARY KEY \
			NOT NULL, 'recipe_indgridient' VARCHAR(150), 'quantity' REAL NOT NULL, \
			FOREIGN KEY (item_id) REFERENCES recipe(recipe_id), \
			FOREIGN KEY (recipe_indgridient) REFERENCES ingridients(ingridient_name));")

#Saving changes in database and closing connection due to multi-thread issues with flask
conn.commit()
db.close()

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
@app.route('/index')
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

	#connect to database
	conn = sqlite3.connect('data.db')
	db = conn.cursor()

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
		db.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?)",
					(username, hashed_passwd, email))

		#save changes
		conn.commit()

		#code for logging user in just after registration
		db.execute("SELECT * FROM users where username = ?", (username,))
		login = db.fetchone()
		print(login)
		session["user_id"] = login[0]
		flash("Registered? Good!", 'alert-success')
		return redirect(url_for("index"))

		#close database
		db.close()
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

@app.route('/_checkUser', methods=['POST'])
def _checkUser():
	"""TODO"""

@app.route('/_checkEmail', methods=['POST'])
def _checkEmail():
	"""TODO"""
