from flask import render_template, flash, redirect
from sqlalchemy import desc

from app import app, forms, db
from app.models import Quotes
from config import POSTS_PER_PAGE


def render_quotes(query, source, page = 1):
    quotes = query.paginate(page, POSTS_PER_PAGE, False)
    return render_template("quotes.html", source = source, quotes = quotes)


@app.route("/newest")
@app.route("/page/<int:page>")
@app.route("/")
def home(page = 1):
    query = Quotes.query.filter_by(pending = False).order_by(desc(Quotes.id))
    return render_quotes(query, "home", page)

@app.route("/top")
@app.route("/top/page/<int:page>")
def top(page = 1):
    query = Quotes.query.filter_by(pending = False).order_by(desc(Quotes.bayesian))
    return render_quotes(query, "top", page)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/submit", methods = ['GET', 'POST'])
def submit():
    form = forms.QuoteSubmission()
    if form.validate_on_submit():
        quote = Quotes(quote = form.quote.data, by = form.submitter.data)
        db.session.add(quote)
        db.session.commit()
        db.session.refresh(quote)
        flash("Submitted quote #{}".format(quote.id))
        return redirect("/")
    return render_template("submit.html", form = form)


if __name__ == "__main__":
    app.run(debug = True)
