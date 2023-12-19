from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, EmailField, PasswordField, SubmitField, TelField, BooleanField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange

# --------------------- SINGUP FORM ---------------------
class SingupForm(FlaskForm):
    # required name field with validator of length and allowed characters
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=20),
        Regexp(r'^[a-zA-ZÀ-ÿ\s\'-]+$', message="Il nome deve contenere solo lettere e spazi.")
    ])

    # required lastname field with validator of length and allowed characters
    lastname = StringField('Lastname', validators=[
        DataRequired(),
        Length(min=2, max=20),
        Regexp(r'^[a-zA-ZÀ-ÿ\s\'-]+$', message="Il cognome deve contenere solo lettere e spazi.")
    ])

    # required phone field with validator of length and numeric format
    phone = TelField('Phone', validators=[
        DataRequired(),
        Length(min=10, max=11, message="Il numero di telefono deve contenere dalle 10 alle 11 cifre."), # DA AGGIUSTARE A 10
        Regexp(r'^\d*$', message="Inserisci solo numeri nel campo telefono.")
    ])

    # required email field with validator to enforce the email format
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Inserisci un indirizzo email valido.")
    ])

    # required password field with length and complexity validator
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=1, max=20), # DA AGGIUSTARE AD 8
        # Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', message="La password deve contenere almeno una lettera minuscola, una lettera maiuscola, un numero e un carattere speciale.")
    ])

    # required boolean field to accept the terms and conditions of the site
    termsandconditions = BooleanField('Accept Terms & Conditions', validators=[DataRequired()])

    # submit type field to send the form and validate it 
    submit = SubmitField('Singup')
# ----------------------------------------------------------------

# -------------------------- LOGIN FORM --------------------------    
class LoginForm(FlaskForm):
    # required email field with validator to enforce the email format
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Inserisci un indirizzo email valido.")
    ])

    # required password field with length and complexity validator
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=1, max=20), # DA AGGIUSTARE AD 8
        # Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', message="La password deve contenere almeno una lettera minuscola, una lettera maiuscola, un numero e un carattere speciale.")
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
        Regexp(r'^[a-zA-ZÀ-ÿ\s\'-]+$', message="Il nome deve contenere solo lettere e spazi.")
    ])

    # required lastname field with validator of length and allowed characters
    lastname = StringField('Lastname', validators=[
        DataRequired(),
        Length(min=2, max=20),
        Regexp(r'^[a-zA-ZÀ-ÿ\s\'-]+$', message="Il cognome deve contenere solo lettere e spazi.")
    ])

    # required phone field with validator of length and numeric format
    phone = TelField('Phone', validators=[
        DataRequired(),
        Length(min=10, max=11, message="Il numero di telefono deve contenere dalle 10 alle 11 cifre."), # DA AGGIUSTARE A 10
        Regexp(r'^\d*$', message="Inserisci solo numeri nel campo telefono.")
    ])

    # required email field with validator to enforce the email format
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Inserisci un indirizzo email valido.")
    ])

    # required password field with length and complexity validator
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=1, max=20), # DA AGGIUSTARE AD 8
        # Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', message="La password deve contenere almeno una lettera minuscola, una lettera maiuscola, un numero e un carattere speciale.")
    ])

    # submit type field to send the form and validate it
    submit = SubmitField('Edit')
# ----------------------------------------------------------------

# --------------------- GIVE FORM ---------------------
class GiveForm(FlaskForm):
    # required starting address field with validator of length and allowed characters
    startPos = StringField('Stai Partendo da...', validators=[
        DataRequired(),
        Length(min=2, max=60)
    ])

    # hidden fields for starting latitude and longitude
    startLat = HiddenField('Latitudine')
    startLng = HiddenField('Longitudine')

   # required seats field with validator for length and numeric format
    seats = IntegerField('Numero di Posti', validators=[
        DataRequired(),
        NumberRange(min=0, max=9, message="Il numero di posti per un'autovettura arriva fino a 9."),
    ])

    # submit type field to send the form and validate it
    submit = SubmitField('Pubblica viaggio')
# ----------------------------------------------------------------

# --------------------- TAKE FORM ---------------------
class TakeForm(FlaskForm):
    # required starting address field with validator of length and allowed characters
    startPos = StringField('Stai Partendo da...', validators=[
        DataRequired(),
        Length(min=2, max=60),
        Regexp(r'^[a-zA-Z0-9\s\-,]+$', message="Inserisci un indirizzo valido per Google Maps.")
    ])

     # hidden fields for starting latitude and longitude
    startLat = HiddenField('Latitudine')
    startLng = HiddenField('Longitudine')

    # required destination address field with validator of length and allowed characters
    endPos = StringField('Vuoi arrivare a...', validators=[
        DataRequired(),
        Length(min=2, max=60),
        Regexp(r'^[a-zA-Z0-9\s\-,]+$', message="Inserisci un indirizzo valido per Google Maps.")
    ])

     # hidden fields for destination latitude and longitude
    endLat = HiddenField('Latitudine')
    endLng = HiddenField('Longitudine')

    # submit type field to send the form and validate it
    submit = SubmitField('Richiedi passaggio')
# ----------------------------------------------------------------