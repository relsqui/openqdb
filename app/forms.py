from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField
from wtforms.validators import Required

class QuoteSubmission(Form):
    quote = TextAreaField("quote", validators = [Required()])
    submitter = StringField("submitter")
