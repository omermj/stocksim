from flask import redirect, render_template, flash, Blueprint, url_for, g
from users.models import User
from trades.models import Trade
from auth.forms import UserEditForm

users = Blueprint("users", __name__, template_folder="templates")


@users.route("/")
def user_home():
    return "User route"


@users.route("/<int:user_id>")
def show_user_dashboard(user_id):
    """Displays user dashboard"""

    # Authenticate user
    if g.user is None or g.user.id != user_id:
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for("auth.login"))

    # Get the user
    user = User.query.get(user_id)

    # Update latest quotes for all open trades
    Trade.update_latest_prices()
    trades = Trade.query.filter(
        Trade.user_id == user_id).order_by(Trade.entry_date).all()

    return render_template("dashboard.html", user=user, trades=trades)


@users.route("/<int:user_id>/profile", methods=["GET", "POST"])
def show_user_profile(user_id):
    """Shows user profile"""

    # Authenticate user
    if g.user is None or g.user.id != user_id:
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for("auth.login"))

    # Get the user
    user = User.query.get(user_id)

    # Get the form
    form = UserEditForm(obj=user)

    # If form data is submitted
    if form.validate_on_submit():
        response = user.edit_profile(first_name=form.first_name.data,
                                     last_name=form.last_name.data,
                                     email=form.email.data)
        print ("#####################")
        print (response)
        if response:
            flash("User profile is updated.", "success")
            return redirect(url_for("users.show_user_dashboard", user_id=user.id))

    return render_template("profile.html", form=form)
