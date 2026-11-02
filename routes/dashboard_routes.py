
from services.dashboard_service import (add_part, get_all_parts, search_part, edit_part as edit_part_function,
                                        get_part_by_part_id, update_stock as update_stock_function,
                                        delete_part as delete_part_function)
from flask import render_template,redirect,url_for,request,Blueprint,flash,current_app
from flask_login import login_required

dash = Blueprint("dash",__name__)

@dash.route("/dashboard",methods=["GET","POST"])
@login_required
def dashboard():
    page = request.args.get("page",1,type=int)
    parts = get_all_parts(page=page)
    return render_template("dashboard.html",parts=parts)

@dash.route("/part/add",methods=["GET","POST"])
@login_required
def add_new_part():
    if request.method == "POST":
        part_id = request.form.get("part_id","")
        part_name = request.form.get("part_name","")

        try:
            add_part(
                part_id=part_id,
                part_name=part_name,
                price=request.form.get("price", ""),
                stock=request.form.get("stock", "")
            )
            flash("New part successfully added.", "success")
            return redirect(url_for("dash.add_new_part"))

        except ValueError as error:
            flash(str(error), "error")

        except Exception:
            current_app.logger.exception("Part couldn't be added.")
            flash("New part cannot be added","error")
            return render_template("add_stock.html")

    return render_template("add_stock.html")

@dash.route("/part/stock")
@login_required
def view_stock():
    page = request.args.get("page", 1, type=int)
    parts = get_all_parts(page=page)
    return render_template("stock.html",parts=parts)

@dash.route("/part/search")
@login_required
def search_parts():
    search_text = request.args.get("q","").strip()

    if not search_text:
        flash("Please enter Part ID or Part Name in Search Bar","error")
        return redirect(url_for("dash.dashboard"))

    page = request.args.get("page",1,type=int)

    parts = search_part(search_text,page=page)


    if parts.total==0:
        flash("Match Not Found","error")

    return render_template("dashboard.html",
                           parts=parts,
                           search_text=search_text,
                           search_performed=True)


@dash.route("/part/<path:part_id>/edit", methods=["GET", "POST"])
@login_required
def edit_part(part_id):
    part = get_part_by_part_id(part_id)

    if part is None:
        flash("Part is not found.", "error")
        return redirect(url_for("dash.dashboard"))

    if request.method == "POST":
        try:
            edit_part_function(
                old_part_id=part_id,
                new_part_id=request.form.get("part_id", "").strip(),
                part_name=request.form.get("part_name", "").strip(),
                price=request.form.get("price", ""),
                stock=request.form.get("stock", "")
            )
            flash("Part successfully edited.", "success")
            return redirect(url_for("dash.dashboard"))

        except ValueError as error:
            flash(str(error), "error")

        except Exception:
            current_app.logger.exception("Part couldn't be edited.")
            flash("Part cannot be edited.", "error")


    return render_template("edit_part.html", part=part)



@dash.route("/part/update-stock",methods=["POST"])
@login_required
def update_stock():
    part_id = request.form.get("part_id","").strip()

    if not part_id:
        flash("Enter the part_id","error")
        return redirect(url_for("dash.dashboard"))

    try:
        update_stock_function(
            part_id=part_id,
            new_stock=request.form.get("stock", "")
        )

        flash("Stock updated successfully.", "success")

    except ValueError as error:
        flash(str(error), "error")

    except Exception:
        current_app.logger.exception("Stock is not updated.")
        flash("An error in updating stock","error")

    return redirect(url_for("dash.dashboard"))

@dash.route("/part/<path:part_id>/delete",methods=["POST"])
@login_required
def delete_part(part_id):

    try:
        delete_part_function(part_id=part_id)
        flash("Part deleted successfully.", "success")


    except ValueError as error:
        flash(str(error), "error")

    except Exception:
        current_app.logger.exception("Part not deleted.")
        flash("Part is not get deleted","error")

    return redirect(url_for("dash.dashboard"))




