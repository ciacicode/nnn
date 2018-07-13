#class for Resume input form
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import SubmitField

class Resume(Form):
    resume = FileField('file')
    submit = SubmitField('Submit')

    # def validate_profile(form, field):
    #     """
    #     Checks there are min 120 words
    #     """
    #     profile = field.data
    #     words = profile.split(" ")
    #     if len(words) < 120:
    #         raise ValidationError('Profile must have more than 120 words. Try harder!')
