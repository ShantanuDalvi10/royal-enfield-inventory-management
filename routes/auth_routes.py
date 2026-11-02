from services.auth_service import register_user,authenticate_user
from flask import Blueprint, current_app, flash ,redirect, render_template, request, url_for
from flask_login import login_required, logout_user, login_user



auth = Blueprint("auth",__name__)

@auth.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        registration_pin = request.form.get("registration_pin","")

        try:
            register_user(
                username=username,
                password=password,
                registration_pin = registration_pin,
                correct_pin=current_app.config.get("REGISTRATION_PIN")
            )
            flash("Registration successful.", "success")
            return redirect(url_for("auth.login"))

        except ValueError as error:
            flash(str(error), "error")

        except Exception:
            current_app.logger.exception("User registration failed")
            flash("Registration failed. Please try again.", "error")



    return render_template("register.html")

@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")

        try:
            user = authenticate_user(username,password)

            login_user(user)

            flash("successfully logged in","success")
            return redirect(url_for("dash.dashboard"))

        except ValueError as error:
            flash(str(error), "error")

        except Exception:
            current_app.logger.exception("User login failed")
            flash("Login failed. Please try again.", "error")

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("successfully logged out","success")
    return redirect(url_for("auth.login"))







