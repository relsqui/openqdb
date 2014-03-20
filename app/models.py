from app import db

class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    upvotes = db.Column(db.Integer, default = 0)
    downvotes = db.Column(db.Integer, default = 0)
    quote = db.Column(db.Text)

    def __repr__(self):
        return "<Quote #{}>".format(self.id)