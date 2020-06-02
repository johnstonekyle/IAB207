
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo


#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name.')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password.')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Enter a valid email.")])

    # ----- will need to change how this works as it does not allow for spaces (e.g. 0412 345 678) -----
    # ----- also currently has no control over min and max character inputs (e.g. phone number of 123) -----
    phone = IntegerField("Phone Number", validators=[InputRequired("Enter a phone number.")])

    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #add buyer/seller - check if it is a buyer or seller hint : Use RequiredIf field
    # ----- Bank details RequiredIf seller is True (need to update database first) -----
    seller = BooleanField("Do you wish to sell products?")

    
    #submit button
    submit = SubmitField("Register")