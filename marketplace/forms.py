
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, IntegerField, BooleanField, SelectField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired


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

ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG', 'bmp'}
#this is the add product form
class AddProductForm(FlaskForm):
    stock = IntegerField("MONTHLY STOCK", validators=[InputRequired()])

    #categories for selector. Must be declared in tuples
    category = SelectField("CATEGORY", choices=[('Teddy Bears','Teddy Bears'), ('Farm Animals','Farm Animals'), ('Cats & Dogs','Cats & Dogs'), ('Wild Animals','Wild Animals'), ('Water Creatures','Water Creatures'), ('Other','Other')])
    
    #currently accepts decimals with more than 2 decimal places. will need to create a regex validator
    price = DecimalField("PRICE", validators=[InputRequired()], places=2)

    #name and desc with a max character length matching the db
    name = StringField("PRODUCT NAME", validators=[InputRequired(), Length(min=1, max=500, message="Max length of 100 characters")])
    description = TextAreaField("DESCRIPTION", validators=[InputRequired(), Length(min=1, max=500, message="Max length of 500 characters")])

    #only the primary should be required while the others are optional
    image_one = FileField("PRIMARY IMAGE", validators=[FileRequired(), FileAllowed(ALLOWED_FILE, message="Only support jpg, JPG, png, PNG, bmp")])
    image_two = FileField("SECOND IMAGE", validators=[FileAllowed(ALLOWED_FILE, message="Only support jpg, JPG, png, PNG, bmp")])
    image_three = FileField("THIRD IMAGE", validators=[FileAllowed(ALLOWED_FILE, message="Only support jpg, JPG, png, PNG, bmp")])

    submit = SubmitField("Confirm")
