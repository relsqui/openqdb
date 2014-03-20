from flask import render_template, flash, redirect
from sqlalchemy import desc

from app import app, forms, db
from app.models import Quotes
from config import POSTS_PER_PAGE

@app.route("/newest")
@app.route("/page/<int:page>")
@app.route("/")
def home(page = 1):
    quotes = Quotes.query.order_by(desc(Quotes.id)).paginate(page, POSTS_PER_PAGE, False)
    return render_template("quotes.html", quotes = quotes)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/submit", methods = ['GET', 'POST'])
def submit():
    form = forms.QuoteSubmission()
    if form.validate_on_submit():
        quote = Quotes(quote = form.quote.data)
        db.session.add(quote)
        db.session.commit()
        db.session.refresh(quote)
        flash("Submitted quote #{}".format(quote.id))
        return redirect("/")
    return render_template("submit.html", form = form)

if __name__ == "__main__":
    app.run(debug = True)
