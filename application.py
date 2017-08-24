from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from passlib.hash import sha256_crypt as crypt
from tempfile import mkdtemp
import sqlite3
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
import re
from flask_jsglue import *
from helpers import *

#adding JSGlue to ensure adding sripts to site
app = Flask(__name__)
JSGlue(app)

#configuring email

app.config.update(dict(
MAIL_SERVER = 'smtp.googlemail.com',
MAIL_PORT = 465,
MAIL_USE_TLS = False,
MAIL_USE_SSL = True,
MAIL_USERNAME = 'pibosz@gmail.com',
MAIL_PASSWORD = 'kzkgop807',
))
mail = Mail(app)

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
			CHECK (meal_type IN ('breakfast', 'dinner', 'supper', 'universal') ));")
#then - create table containing recipe_items - ingridients for particular recipe
db.execute("CREATE TABLE IF NOT EXISTS 'recipe_items' ('item_id' INTEGER PRIMARY KEY \
			AUTOINCREMENT NOT NULL, 'recipe_ingridient' VARCHAR(150), \
			meal_id INTEGER NOT NULL, user_id INTEGER NOT NULL, \
			FOREIGN KEY (meal_id) REFERENCES recipe(recipe_id), \
			FOREIGN KEY (user_id) REFERENCES users(id))")

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
# configuring secret key for url tokenizer
app.config["SECRET_KEY"] = "kl3zbytomash"
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

Session(app)

@app.route('/')
@app.route('/index')
def index():
	flash('TODO', 'alert-info')
	return render_template('index.html')

@app.route('/check_recipes')
@login_required
def check_recipes():
	conn = sqlite3.connect('data.db')
	db = conn.cursor()
	user_id = session["user_id"]

	db.execute("SELECT * FROM recipe WHERE user_id=?", (user_id,))
	rows = db.fetchall()
	data=[]
	print(rows)

	for row in rows:
		data.append({
		"name": row[2],
		"recipe_id": row[0]
		})

	print(data)
	flash('TODO', 'alert-info')
	return render_template('check_recipes.html', rows=data)

@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
	conn = sqlite3.connect('data.db')
	db = conn.cursor()

	if request.method == "POST":
		dishName = request.form.get("dishName")
		recipeItems = request.form.get("recipeItems")
		mealType = request.form.get("mealType")
		recipeHowTo = request.form.get("recipeHowTo")
		itemsList = recipeItems.split(", ")
		user_id = session["user_id"]

		if not dishName:
			flash('Please enter recipe name', 'alert-danger')
			return render_template("add_recipe.html")
		if not recipeItems:
			flash('Please enter the recipe indgridients', 'alert-danger')
			return render_template("add_recipe.html")
		if not recipeHowTo:
			flash('Please enter the recipe', 'alert-danger')
			return render_template("add_recipe.html")

		db.execute("INSERT INTO recipe (user_id, title, prepare, meal_type) \
					VALUES (?, ?, ?, ?);", (user_id, dishName, recipeHowTo, mealType))

		meal_id = db.lastrowid

		for item in itemsList:
			db.execute("INSERT INTO recipe_items (meal_id, recipe_ingridient, user_id) \
						VALUES (?, ?, ?);", (meal_id, item, user_id))

		conn.commit()
		db.close()

		flash('You\'ve added {0} recipe!'.format(dishName), 'alert-success')
		return redirect(url_for("index"))
	else:
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

		#validate user's entries. Back-end validation in case that user turns off js
		if not username:
			flash('Please enter ther user name', 'alert-danger')
			return render_template("register.html")
		if check_database("username", username) == False:
			flash('Username already taken', 'alert-danger')
			return render_template("register.html")
		if not password_1:
			flash('Please enter the password', 'alert-danger')
			return render_template("register.html")
		if not password_2:
			flash('Please repeat the password', 'alert-danger')
			return render_template("register.html")
		if password_1 != password_2:
			flash('Passwords must be the same', 'alert-danger')
			return render_template("register.html")
		if not email:
			flash('Please enter e-mail address', 'alert-danger')
			return render_template("register.html")
		if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
			#email check by regular expression. More on http://emailregex.com/
			flash('Please enter valid e-mail address', 'alert-danger')
			return render_template("register.html")
		if check_database("email", email) == False:
			flash('Email already registered', 'alert-danger')
			return render_template("register.html")

		#hash password
		hashed_passwd = crypt.hash(password_1)

		#insert valid user into users table
		db.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?)",
					(username, hashed_passwd, email))

		#save changes
		conn.commit()

		#send confirmation email
		site_address = "http://127.0.0.1:5000/confirm/"
		token = ts.dumps(email, salt='email-confirm-key')
		text = "Hello, this is confirmation link: %s%s" % (site_address, token)
		msg = Message('Confirmation - Meal planner', sender='pibosz@gmail.com',
					  body=text,
					  recipients=[email])
		mail.send(msg)

		#inform users about confirmation e-mail
		flash("Confirmation link was sent to %s" % email, 'alert-success')
		return redirect(url_for("index"))

		#close database
		db.close()
	else:
		return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
	#connect to database
	conn = sqlite3.connect('data.db')
	db = conn.cursor()

	#server-side validation
	if request.method == "POST":
		login = request.form.get("login")
		password = request.form.get("password")

		if login == "":
			flash('Please enter ther login', 'alert-danger')
			return render_template("login.html")
		if password == "":
			flash('Please enter ther password', 'alert-danger')
			return render_template("login.html")

		db.execute("SELECT * FROM users WHERE username=?", (login,))
		login_result = db.fetchone()

		if len(login_result) != 5 \
		or not pwd_context.verify(password, login_result[2]):
			flash('Invalid login or password', 'alert-danger')
			return redirect(url_for("login"))
		elif login_result[4] != 1:
			flash('Account is not activated yet. Please check your email.', \
			 	  'alert-danger')
			return redirect(url_for("login"))
		else:
			session["user_id"] = login_result[0]
			return redirect(url_for("index"))

	else:
		return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
	"""Log user out."""
	# forget any user_id
	session.clear()

	# redirect user to login form
	return redirect(url_for("index"))

@app.route('/confirm/<token>')
def confirm(token):

	conn = sqlite3.connect('data.db')
	db = conn.cursor()

	try:
		email = ts.loads(token, salt='email-confirm-key', max_age=86400)
	except:
		flash("Email not found. Activation link may be expired", 'alert-danger')
		return redirect(url_for("index"))

	#Set user as veryfied
	db.execute("UPDATE users SET veryfied = 1 WHERE email=?", (email,))
	conn.commit()

	#Login veryfied user
	db.execute("SELECT username FROM users WHERE email=?", (email,))
	user = db.fetchone()
	print(user)
	session["user_id"] = user
	flash("You confirmed your account!", 'alert-success')
	return redirect(url_for("index"))

	#close database
	db.close()

@app.route('/edit/<recipe_id>', methods=["POST", "GET"])
@login_required
def edit(recipe_id):
	if request.method == "POST":
		flash("Not yet my friend, not yet :)", 'alert-danger')
		return redirect(url_for("index"))
	else:
		conn = sqlite3.connect('data.db')
		db = conn.cursor()

		db.execute("SELECT * FROM recipe WHERE recipe_id=?", (recipe_id,))
		recipe_data = db.fetchone()
		recipe_data = list(recipe_data)
		r_title = recipe_data[2]
		r_prepare = recipe_data[3]
		r_type = recipe_data[4]

		db.execute("SELECT recipe_ingridient FROM recipe_items WHERE meal_id=?", (recipe_id,))
		r_items = db.fetchall()
		r_items = [x[0] for x in r_items]
		print(r_items)
		r_items = ", ".join(r_items)

		breakfast = ""
		dinner = ""
		supper = ""
		universal = ""

		if r_type == "breakfast":
			breakfast = "active"
		elif r_type == "dinner":
			dinner = "active"
		elif r_type == "supper":
			supper = "active"
		else:
			universal = "active"

		return render_template('edit_recipe.html', recipe_id=recipe_id,
								title=r_title, prepare=r_prepare, items=r_items,
								breakfast=breakfast, dinner=dinner,
								supper=supper, universal=universal)

@app.route('/_checkUser', methods=['POST'])
def _checkUser():
	username = request.form["username"]
	element = "username"
	user_test = check_database(element, username)
	return jsonify(result=user_test)


@app.route('/_checkEmail', methods=['POST'])
def _checkEmail():
	email = request.form["email"]
	element = "email"
	email_test = check_database(element, email)
	return jsonify(result=email_test)
