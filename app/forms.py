from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField, IntegerField
from wtforms.validators import Required

class QuoteSubmission(Form):
    quote = TextAreaField("quote", validators = [Required()])
    submitter = StringField("submitter")

class DateRange(Form):
    days = IntegerField("days", default = 14)

class Search(Form):
    needle = StringField("needle")
