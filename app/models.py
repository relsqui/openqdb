from datetime import datetime

from app import db


class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    quote = db.Column(db.Text)
    by = db.Column(db.String(255))
    date = db.Column(db.DateTime, default = datetime.now())
    comment = db.Column(db.Text, default = "")
    pending = db.Column(db.Boolean, default = True)
    upvotes = db.Column(db.Integer, default = 0)
    downvotes = db.Column(db.Integer, default = 0)
    bayesian = db.Column(db.Float, default = 0)

    def __repr__(self):
        return "<Quote #{}>".format(self.id)
