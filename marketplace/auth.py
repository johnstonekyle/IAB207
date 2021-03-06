from flask import Blueprint, render_template, request, url_for, redirect, flash
from .forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from . import db
from .models import User


bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    error = None
    if(login_form.validate_on_submit()):
        #get form data
        user_name = login_form.user_name.data
        password = login_form.password.data

        #query database for user
        u1 = User.query.filter_by(username=user_name).first()

        #if user doesnt exist then error
        if u1 is None: 
            error="Incorrect username"

        #if password doesnt match then error
        elif not check_password_hash(u1.password_hash, password):
            error = "Incorrect password"

        if error is None: #if no errors then login the user and redirect
            login_user(u1)
            return redirect(url_for("main.index"))
        else:
            flash(error) #display errors in html


    return render_template("user.html", form=login_form, heading="Login")


@bp.route("/register", methods=["GET", "POST"])
def register():
    register = RegisterForm()
    if (register.validate_on_submit()):
        #get username, password and email from the form
        uname = register.user_name.data
        pwd = register.password.data
        email = register.email_id.data
        pnum = register.phone.data
        status = register.seller.data
        bankdetails = register.bankdetails.data

        #try and see if user already exists
        u1 = User.query.filter_by(username=uname).first()
        if u1:
            flash("Username already exists! Please login.")
            return redirect(url_for("auth.login"))
        
        #if bank details are empty but the user wants to sign up as a seller, provide error
        if (bankdetails == '') and (register.seller.data == True):
            flash("To register as a seller, you must provide your bank details.")
            return redirect(url_for("auth.register"))
        
        #hash the plaintext password
        pwd_hash = generate_password_hash(pwd)

        #create new user object
        new_user = User(username=uname, password_hash=pwd_hash, email=email, phone=pnum, seller=status, bank_account=bankdetails)

        #save to database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("main.index"))
    
    else:
        return render_template("user.html", form=register, heading="Register")



@bp.route("/logout")
@login_required
def logout():
    #log out user and redirect
    logout_user()
    return redirect(url_for("main.index"))