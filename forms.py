from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, EmailField, PasswordField, SubmitField, TelField, BooleanField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange

# --------------------- SINGUP FORM ---------------------
class SingupForm(FlaskForm):
    # required name field with validator of length and allowed characters
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=20),
        Regexp(r'^[a-zA-ZÀ-ÿ\s\'-]+$', message="The name must contain only letters and spaces.")
    ])

    # required lastname field with validator of length and allowed characters
    lastname = StringField('Lastname', validators=[
        DataRequired(),
        Length(min=2, max=20),
        Regexp(r'^[a-zA-ZÀ-ÿ\s\'-]+$', message="The last name must contain only letters and spaces.")
    ])

    # required phone field with validator of length and numeric format
    phone = TelField('Phone', validators=[
        DataRequired(),
        Length(min=10, max=11, message="The telephone number must contain 10 to 11 digits."),
        Regexp(r'^\d*$', message="Enter only numbers in the phone field.")
    ])

    # required email field with validator to enforce the email format
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Enter a valid email address.")
    ])

    # required password field with length and complexity validator
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=1, max=20),
        # Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]+$', message="The password must contain at least one lowercase letter, one uppercase letter, one number, and one special character.")
    ])

    # required boolean field to accept the terms and conditions of the site
    # termsandconditions = BooleanField('Accept Terms & Conditions', validators=[DataRequired()])

    # submit type field to send the form and validate it 
    submit = SubmitField('Sing up')
# ----------------------------------------------------------------

# -------------------------- LOGIN FORM --------------------------    
class LoginForm(FlaskForm):
    # required email field with validator to enforce the email format
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Enter a valid email address.")
    ])

    # required password field with length and complexity validator
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=1, max=20), # DA AGGIUSTARE AD 8
        # Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]+$', message="The password must contain at least one lowercase letter, one uppercase letter, one number, and one special character.")
    ])

    # campo booleano per far scegliere all'utente se rimanere loggato oppure no
    rememberme = BooleanField('Remember Me')

    # submit type field to send the form and validate it
    submit = SubmitField('Login')
# ----------------------------------------------------------------

# --------------------------- INFO FORM --------------------------
class InfoForm(FlaskForm):
    # required name field with validator of length and allowed characters
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=20),
        Regexp(r'^[a-zA-ZÀ-ÿ\s\'-]+$', message="The name must contain only letters and spaces.")
    ])

    # required lastname field with validator of length and allowed characters
    lastname = StringField('Lastname', validators=[
        DataRequired(),
        Length(min=2, max=20),
        Regexp(r'^[a-zA-ZÀ-ÿ\s\'-]+$', message="The last name must contain only letters and spaces.")
    ])

    # required phone field with validator of length and numeric format
    phone = TelField('Phone', validators=[
        DataRequired(),
        Length(min=10, max=11, message="The telephone number must contain 10 to 11 digits."),
        Regexp(r'^\d*$', message="Enter only numbers in the phone field.")
    ])

    # required email field with validator to enforce the email format
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Enter a valid email address.")
    ])

    # required password field with length and complexity validator
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=1, max=20),
        # Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]+$', message="The password must contain at least one lowercase letter, one uppercase letter, one number, and one special character.")
    ])

    # submit type field to send the form and validate it
    submit = SubmitField('Edit')
# ----------------------------------------------------------------

# --------------------- GIVE FORM ---------------------
class GiveForm(FlaskForm):
    # required starting address field with validator of length and allowed characters
    startPos = StringField('departure', validators=[
        DataRequired(),
        Length(min=2, max=60)
    ])

    # hidden fields for starting latitude and longitude
    startLat = HiddenField('Latitudine')
    startLng = HiddenField('Longitudine')

   # required seats field with validator for length and numeric format
    seats = IntegerField('seat available', validators=[
        DataRequired(),
        NumberRange(min=0, max=8, message="The number of passenger seats for a passenger car is up to 8."),
    ])

    # submit type field to send the form and validate it
    submit = SubmitField('give ride')
# ----------------------------------------------------------------

# --------------------- TAKE FORM ---------------------
class TakeForm(FlaskForm):
    # required starting address field with validator of length and allowed characters
    startPos = StringField('departure', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])

     # hidden fields for starting latitude and longitude
    startLat = HiddenField('Latitudine')
    startLng = HiddenField('Longitudine')

    # required destination address field with validator of length and allowed characters
    endPos = StringField('destination', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])

     # hidden fields for destination latitude and longitude
    endLat = HiddenField('Latitudine')
    endLng = HiddenField('Longitudine')

    # submit type field to send the form and validate it
    submit = SubmitField('request ride')
# ----------------------------------------------------------------