from flask import redirect, render_template, flash, Blueprint, url_for
from trades.models import db, Trade

trades = Blueprint("trades", __name__, template_folder="templates")


@trades.route("/")
def user_home():
    return "Trade route"
