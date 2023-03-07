from flask import redirect, render_template, flash, url_for
from users.models import User
from auth.forms import UserEditForm, ChangePasswordForm
from users.forms import ChangeAccountSettings


class Views(object):
    """Utilities Class for User"""

    @classmethod
    def show_and_edit_profile(cls, user_id):
        """Shows user and edits user profile"""

        user = User.query.get(user_id)
        form = UserEditForm(obj=user)

        if form.validate_on_submit():
            response = user.edit_profile(email=form.email.data,
                                         first_name=form.first_name.data,
                                         last_name=form.last_name.data)
            if response:
                flash("User profile is updated.", "success")
                return redirect(url_for("users.show_user_dashboard", user_id=user.id))
            else:
                flash(
                    "Error updating the profile. Please try again.",
                    "danger")

        return render_template("profile.html", form=form)

    @classmethod
    def show_and_change_password(cls, user_id):
        """Show change password form and change user password when form is submitted"""

        user = User.query.get(user_id)
        form = ChangePasswordForm()

        # If form data is submitted and validated, change password, else return error
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

    @classmethod
    def show_and_change_settings(cls, user_id):
        """Show change settings form and update settings if form is submitted"""

        user = User.query.get(user_id)
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
