
from Functions.dashboard_functions import (add_part,get_all_parts,search_part,edit_part as edit_part_function,
                                           get_part_by_part_id,update_stock as update_stock_function,
                                           delete_part as delete_part_function)
from flask import render_template,redirect,url_for,request,Blueprint,flash,current_app
from flask_login import login_required

dash = Blueprint("dash",__name__)

@dash.route("/part/add",methods=["GET","POST"])
@login_required
def add_new_part():
    if request.method == "POST":
        part_id = request.form.get("part_id","")
        part_name = request.form.get("part_name","")


        try:
            price = float(request.form.get("price", ""))
            stock = int(request.form.get("stock", ""))

            if price<0 or stock<0:
                raise ValueError

            success,message = add_part(
                part_id=part_id,
                part_name=part_name,
                price=price,
                stock=stock
            )
        except ValueError:
            flash("Please enter valid positive numbers.", "error")
            return render_template("add_stock.html")

        except Exception:
            current_app.logger.exception("Part couldn't be added.")
            flash("New part cannot be added","error")
            return render_template("add_stock.html")

        if success:
            flash("New part successfully added.","success")
            return redirect(url_for("dash.add_new_part"))

        flash(message,"error")

    return render_template("add_stock.html")

@dash.route("/part/stock")
@login_required
def view_stock():
    parts = get_all_parts()
    return render_template("stock.html",parts=parts)

@dash.route("/part/search")
@login_required
def search_parts():
    search_text = request.args.get("q","")

    if not search_text:
        flash("Please enter Part ID or Part Name in Search Bar","error")
        return redirect(url_for("auth.dashboard"))

    searched_text = search_part(search_text)
    parts = get_all_parts()

    if not searched_text:
        flash("Match Not Found","error")

    return render_template("dashboard.html",
                           searched_part=searched_text,
                           parts=parts,
                           search_performed=True)

@dash.route("/part/<string:part_id>/edit",methods=["GET","POST"])
@login_required
def edit_part(part_id):
    part = get_part_by_part_id(part_id)

    if part is None:
        flash("Part is not found.","error")
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        try:
            price = float(request.form.get("price", ""))
            stock = int(request.form.get("stock", ""))
            if price < 0 or stock < 0 :
                raise ValueError
        except ValueError:
            flash("Please enter valid positive numbers.", "error")
            return render_template("edit_part.html", part=part)

        success,message = edit_part_function(
            old_part_id=part_id,
            new_part_id=request.form.get("part_id","").strip(),
            part_name=request.form.get("part_name","").strip(),
            price=price,
            stock=stock,
        )

        if success:
            flash(message,"success")
            return redirect(url_for("auth.dashboard"))

        flash(message,"error")
    return render_template("edit_part.html",part=part)


@dash.route("/part/update-stock",methods=["POST"])
@login_required
def update_stock():
    part_id = request.form.get("part_id","").strip()
    if not part_id:
        flash("Enter the part_id","error")
        return redirect(url_for("auth.dashboard"))

    try:
        stock = int(request.form.get("stock",""))
        if stock < 0:
            raise ValueError

        success,message = update_stock_function(part_id=part_id,new_stock=stock)
        flash(message,"success" if success else "error")
    except ValueError:
        flash("Enter Positive Number","error")

    except Exception:
        current_app.logger.exception("Stock is not updated.")
        flash("An error in updating stock","error")

    return redirect(url_for("auth.dashboard"))

@dash.route("/part/<string:part_id>/delete",methods=["POST"])
@login_required
def delete_part(part_id):

    try:
        success,message = delete_part_function(part_id=part_id)

        if success:
            flash(message,"success")
        else:
            flash(message,"error")

    except Exception:
        current_app.logger.exception("Part not deleted.")
        flash("Part is not get deleted","error")

    return redirect(url_for("auth.dashboard"))




