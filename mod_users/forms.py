from email.mime import image
from flask_wtf import FlaskForm
from wtforms import EmailField
from wtforms import PasswordField , StringField , TextAreaField , FileField
from wtforms.validators import DataRequired



class LoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username= StringField(validators=[DataRequired()])
    email= EmailField(validators=[DataRequired()])
    password= PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired()])
    # phone_number = StringField(validators=[DataRequired()])


class SliderForm(FlaskForm):
    slider_title = StringField(validators=[DataRequired()])
    slider_image = FileField(validators=[DataRequired()])
    slider_link = StringField(validators=[DataRequired()])


class CardForm(FlaskForm):
    mahsol_count = StringField(validators=[DataRequired()])
    mahsol_name = StringField(validators=[DataRequired()])
    mahsol_title = StringField(validators=[DataRequired()])
    
class MonasebatForm(FlaskForm):
    monasebat_title = StringField(validators=[DataRequired()])
    monasebat_image = FileField(validators=[DataRequired()])
    monasebat_link = StringField(validators=[DataRequired()])


class BlogForm(FlaskForm):
    blog_title = StringField(validators=[DataRequired()])
    blog_content = TextAreaField(validators=[DataRequired()])
    blog_metacontent = StringField(validators=[DataRequired()])
    blog_writer = StringField(validators=[DataRequired()])
    blog_image = FileField(validators=[DataRequired()])
    blog_date = StringField(validators=[DataRequired()])
    blog_group_mortabet = StringField(validators=[DataRequired()])


