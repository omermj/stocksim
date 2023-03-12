from flask import redirect, render_template, Blueprint, url_for, g
from auth.login import Login
from users.dashboard import Dashboard
from users.views import Views

users = Blueprint("users", __name__, template_folder="templates")
views = Views()


@users.route("/")
@Login.require_login
def user_home():
    """Shows user dashboard if logged in, else show login page"""

    return redirect(url_for("users.show_user_dashboard", user_id=g.user.id))


@users.route("/<int:user_id>")
@Login.require_login
def show_user_dashboard(user_id):
    """Displays user dashboard"""

    return render_template("dashboard.html",
                           dashboard=Dashboard(user_id=user_id))


@users.route("/<int:user_id>/profile", methods=["GET", "POST"])
@Login.require_login
def show_user_profile(user_id):
    """Show user profile"""

    return views.show_and_edit_profile(user_id=user_id)


@users.route("/<int:user_id>/changepassword", methods=["GET", "POST"])
@Login.require_login
def change_password(user_id):
    """Change user password"""

    return views.show_and_change_password(user_id=user_id)


@users.route("/<int:user_id>/settings", methods=["GET", "POST"])
@Login.require_login
def change_settings(user_id):
    """Chage user account settings (depost/withdraw funds)"""

    return views.show_and_change_settings(user_id=user_id)
