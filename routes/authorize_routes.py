from Functions.Authentication_Functions import register_user,authenticate_user
from flask import Blueprint, current_app, flash ,redirect, render_template, request, url_for
from flask_login import login_required, logout_user, login_user
from Functions.dashboard_functions import get_all_parts


auth = Blueprint("auth",__name__)

@auth.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        registration_pin = request.form.get("registration_pin","")

        try:
            success,message = register_user(
                username=username,
                password=password,
                registration_pin = registration_pin,
                correct_pin=current_app.config.get("REGISTRATION_PIN")
            )
            if success:
                flash(message, "success")
                return redirect(url_for("auth.login"))
            flash(message, "error")

        except Exception:
            current_app.logger.exception("User registration failed")
            flash("Registration failed. Please try again.", "error")



    return render_template("register.html")

@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")

        if not username or not password:
            flash("Please Complete the required fields","error")
            return render_template("login.html")

        user = authenticate_user(username,password)

        if user == None:
            flash("Incorrect User or Password","error")
            return render_template("login.html")

        login_user(user)
        flash("successfully logged in","success")
        return redirect(url_for("auth.dashboard"))

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("successfully logged out","success")
    return redirect(url_for("auth.login"))

@auth.route("/dashboard",methods=["GET","POST"])
@login_required
def dashboard():
    parts = get_all_parts()
    return render_template("dashboard.html",parts=parts)





