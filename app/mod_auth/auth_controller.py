from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Sign In
@mod_auth.route('/signin', methods=['GET', 'POST'])
def signin():
    return render_template("auth/signin.html", name="ExpressPredict | SignIn")


# Sign Up
@mod_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("auth/signup.html", name="ExpressPredict | SignUp")