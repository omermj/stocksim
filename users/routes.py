from flask import redirect, render_template, flash, Blueprint, url_for
from users.models import db, User

users = Blueprint("users", __name__, template_folder="templates")


@users.route("/")
def user_home():
    return "User route"
