from flask import redirect, render_template, flash, Blueprint, url_for
from watchlists.models import db, Watchlist

watchlists = Blueprint("watchlists", __name__, template_folder="templates")


@watchlists.route("/")
def watchlist_home():
    return "Watchlist route"

