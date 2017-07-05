from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from passlib.hash import sha256_crypt as crypt
from tempfile import mkdtemp
from flask_jsglue import *
from helpers import *

#adding JSGlue to ensure adding sripts to site
jsglue = JSGlue()
app = Flask(__name__)
jsglue.init_app(app)

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
def check_recipes():
  flash('TODO', 'alert-info')
  return render_template('check_recipes.html')

@app.route('/add_recipe')
def add_recipe():
  flash('TODO', 'alert-info')
  return render_template('add_recipe.html')

@app.route('/generate_meals')
def generate_meals():
  flash('TODO', 'alert-info')
  return render_template('generate_meals.html')

@app.route('/register')
def register():
  flash('TODO', 'alert-info')
  return render_template('register.html')

@app.route('/login')
def login():
  flash('TODO', 'alert-info')
  return render_template('login.html')
