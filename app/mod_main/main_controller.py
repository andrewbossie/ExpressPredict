from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/hub')

# Landing Page
@mod_main.route('/landing', methods=['GET'])
def landing():
    return render_template("main/landing.html")