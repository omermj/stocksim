from flask import redirect, render_template, flash, Blueprint, url_for, g, request, jsonify
from watchlists.models import db, Watchlist
from watchlists.forms import CreateWatchlistForm
from auth.login import Login


watchlists = Blueprint("watchlists", __name__,
                       template_folder="templates", static_folder="static")


@watchlists.route("/", methods=["GET", "POST"])
@Login.require_login
def watchlist_home():
    """Show all watchlists"""

    # Get create watchlist form
    form = CreateWatchlistForm()

    # If form is submitted, add watchlist
    if form.validate_on_submit():
        watchlist = Watchlist.create(name=form.name.data,
                                     description=form.description.data,
                                     user_id=g.user.id)
        if watchlist:
            flash("New watchlist is successfully created.", "success")
        else:
            flash("Error creating watchlist.", "danger")
        return redirect(url_for("watchlists.watchlist_home"))

    return render_template("watchlists.html", watchlists=g.user.watchlists,
                           form=form)


@watchlists.route("/<int:watchlist_id>", methods=["GET", "POST"])
@Login.require_login
def show_watchlist(watchlist_id):
    """Show details page for watchlist"""

    # Get the watchlist and watchlist form for editing
    watchlist = Watchlist.query.get(watchlist_id)
    form = CreateWatchlistForm(obj=watchlist)

    # If edit watchlist form is submitted, update watchlist in db
    if form.validate_on_submit():
        response = watchlist.edit(new_name=form.name.data,
                                  new_description=form.description.data)
        if response:
            flash("Watchlist has been successfully edited.", "success")

        else:
            flash("There was an error editing the watchlist. Please try again.",
                  "danger")

    return render_template("watchlist_details.html",
                           watchlist=watchlist,
                           stocks=watchlist.get_all_stocks(),
                           form=form)


@watchlists.route("/<int:watchlist_id>", methods=["DELETE"])
@Login.require_login
def remove_watchlist(watchlist_id):
    """Remove watchlist"""

    watchlist = Watchlist.query.get(watchlist_id)

    if Watchlist.remove(watchlist):
        return jsonify({"result": "success"})
    else:
        return jsonify({"result": "error"})


# @watchlists.route("/<int:watchlist_id>", methods=["PUT"])
# @Login.require_login
# def edit_watchlist(watchlist_id):
#     """Edit watchlist"""

#     watchlist = Watchlist.query.get(watchlist_id)
