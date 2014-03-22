from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, request
from sqlalchemy import desc

from app import app, forms, db
from app.models import Quotes
from config import POSTS_PER_PAGE


def render_quotes(query, page = 1, bayesian_sort = True, template = "quotes.html", **kwargs):
    quotes = query.filter_by(pending = False)
    if bayesian_sort:
        quotes = quotes.order_by(desc(Quotes.bayesian))
    quotes = quotes.paginate(page, POSTS_PER_PAGE, False)
    old_args = dict(request.view_args)
    if "page" in old_args:
        del old_args["page"]
    return render_template(template, quotes = quotes, searchform = forms.Search(), old_args = old_args, **kwargs)

@app.route("/<int:quote>")
def onequote(quote):
    query = Quotes.query.filter_by(id = quote)
    return render_quotes(query)

@app.route("/about")
def about():
    return render_template("about.html", searchform = forms.Search())

@app.route("/submit", methods = ['GET', 'POST'])
def submit():
    form = forms.QuoteSubmission()
    if form.validate_on_submit():
        quote = Quotes(quote = form.quote.data, by = form.submitter.data)
        db.session.add(quote)
        db.session.commit()
        db.session.refresh(quote)
        flash("Submitted quote #{}".format(quote.id))
        return redirect(url_for("home"))
    return render_template("submit.html", form = form, searchform = forms.Search())

@app.route("/newest")
@app.route("/newest/page/<int:page>")
@app.route("/page/<int:page>")
@app.route("/")
def home(page = 1):
    numeric_queries = [k for k in request.args.keys() if k.isdigit()]
    if numeric_queries:
        return onequote(numeric_queries[0])
    query = Quotes.query.order_by(desc(Quotes.id))
    return render_quotes(query, page, bayesian = False)

@app.route("/top/page/<int:page>")
@app.route("/top")
def top(page = 1):
    return render_quotes(Quotes.query, page)

@app.route("/recent/days/<int:days>/page/<int:page>", methods = ['GET', 'POST'])
@app.route("/recent/page/<int:page>", methods = ['GET', 'POST'])
@app.route("/recent/days/<int:days>", methods = ['GET', 'POST'])
@app.route("/recent", methods = ['GET', 'POST'])
def recent(page = None, days = None):
    form = forms.DateRange()
    if form.validate_on_submit():
        return redirect(url_for("recent", days = form.days.data, page = page))
    if not days:
        days = form.days.default
    if not page:
        page = 1
    quotes = Quotes.query.filter(Quotes.date > datetime.now() - timedelta(days))
    return render_quotes(quotes, page, template = "recent.html", days = days, form = form)


@app.route("/search", methods = ['GET', 'POST'])
def splitsearch():
    form = forms.Search()
    if not form.validate_on_submit():
        return redirect(url_for("home"))
    if form.needle.data.isdigit():
        return redirect(url_for("onequote", quote = form.needle.data))
    else:
        return redirect(url_for("search", needle = form.needle.data))

@app.route("/search/<string:needle>")
@app.route("/search/<string:needle>/page/<int:page>")
def search(page = 1, needle = None):
    query = Quotes.query.filter(Quotes.quote.contains(needle))
    return render_quotes(query, page)


if __name__ == "__main__":
    app.run(debug = True)
