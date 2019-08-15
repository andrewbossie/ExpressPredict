from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for


# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.signin_form import SigninForm
from app.mod_auth.signup_form import SignupForm

# Import module models (i.e. User)
# from app.mod_auth.Users import User


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Sign In
@mod_auth.route('/signin', methods=['GET', 'POST'])
def signin():

    # If sign in form is submitted
    signin_form = SigninForm(request.form)

    # Verify the sign in form
    if signin_form.validate_on_submit():

        # user = User.query.filter_by(email=form.email.data).first()

        # if user and check_password_hash(user.password, form.password.data):

        session['user_id'] = "Andrew"

        return redirect(url_for('home'))

    return render_template("auth/login.html", header="ExpressPredict | SignIn", form=signin_form)


# Sign Up
@mod_auth.route('/signup', methods=['GET', 'POST'])
def signup():

    # If sign in form is submitted
    signup_form = SignupForm(request.form)

    # Verify the sign in form
    if signup_form.validate_on_submit():

        # If valid new user & created 
        session['user_id'] = "Andrew"

        # flash('Welcome %s' % user.name)

        return redirect(url_for('auth.signin'))

    return render_template("auth/signup.html", header="ExpressPredict | SignUp", form=signup_form)


# Sign Up
@mod_auth.route('/logout', methods=['GET', 'POST'])
def logout():

    # Logout
    session['user_id'] = ""

    return redirect(url_for('/'))