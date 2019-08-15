from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for


mod_main = Blueprint('main', __name__)

# Landing Page
@mod_main.route('/', methods=['GET'])
def landing():
    return render_template("main/landing.html", header="EP | Welcome")

# Home Page
@mod_main.route('/home', methods=['GET'])
def home():
    return render_template("main/home.html", header="EP | Welcome")