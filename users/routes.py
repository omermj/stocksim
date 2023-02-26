from flask import redirect, render_template, flash, Blueprint, url_for, g
from users.models import User
from trades.models import Trade
from auth.forms import UserEditForm, ChangePasswordForm
from users.forms import ChangeAccountSettings

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

    # Get 5 recent open trades
    open_trades = Trade.query.filter(
        (Trade.user_id == user_id) & (Trade.status == "open")).order_by(Trade.entry_date).limit(5).all()

    # # Get 5 recent closed trades
    closed_trades = Trade.query.filter(
        (Trade.user_id == user_id) & (Trade.status == "closed")).order_by(Trade.entry_date).limit(5)

    return render_template("dashboard.html", user=user, open_trades=open_trades, closed_trades=closed_trades)


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
        response = user.edit_profile(first_name=form.first_name.data.strip(),
                                     last_name=form.last_name.data.strip(),
                                     email=form.email.data.strip())
        if response:
            flash("User profile is updated.", "success")
            return redirect(url_for("users.show_user_dashboard", user_id=user.id))

    return render_template("profile.html", form=form)


@users.route("/<int:user_id>/changepassword", methods=["GET", "POST"])
def change_password(user_id):
    """Shows user profile"""

    # Authenticate user
    if g.user is None or g.user.id != user_id:
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for("auth.login"))

    # Get the user
    user = User.query.get(user_id)

    # Get the form
    form = ChangePasswordForm()

    # If form data is submitted
    if form.validate_on_submit():

        response = user.change_password(username=user.username,
                                        current_password=form.current_password.data,
                                        new_password=form.new_password.data)
        if response:
            flash("Password is updated.", "success")
            return redirect(url_for("users.show_user_dashboard", user_id=user.id))
        else:
            flash("The current password is incorrect. Please try again.", "danger")

    return render_template("change_password.html", form=form)


@users.route("/<int:user_id>/settings", methods=["GET", "POST"])
def change_settings(user_id):
    """Chage user account settings (depost/withdraw funds)"""

    # Authenticate user
    if g.user is None or g.user.id != user_id:
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for("auth.login"))

    # Get the user
    user = User.query.get(user_id)

    # Get the form
    form = ChangeAccountSettings()

    if form.validate_on_submit():

        if form.type.data == "deposit":
            new_balance = user.deposit_funds(form.amount.data)
        else:
            new_balance = user.withdraw_funds(form.amount.data)

        if new_balance == False:
            flash("An error occured while updating the balance.", "danger")
            return render_template("settings.html", user=user, form=form)
        else:
            flash("Balance is successfully updated.", "success")
            return redirect(url_for("users.show_user_dashboard", user_id=user.id))

    return render_template("settings.html", user=user, form=form)
