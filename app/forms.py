from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, PasswordField, FileField, SelectField, HiddenField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import User
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists. Please choose another.')

class UploadForm(FlaskForm):
    title = StringField('Image Title', validators=[DataRequired()])
    image = FileField('Image File', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Upload')


class PostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired()])
    subtitle = StringField('Post Subtitle', validators=[DataRequired()])
    image_id = HiddenField('Select an Image', validators=[DataRequired()])
    submit = SubmitField('Create Post')

class ToolResultForm(FlaskForm):
    tool = HiddenField('Tool', validators=[DataRequired()])
    threshold = HiddenField('Threshold')
    input_image_id = HiddenField('Input Image')
    output_image_dataurl = HiddenField('Output Image Data URL', validators=[DataRequired()])
    submit = SubmitField('Save your result')
