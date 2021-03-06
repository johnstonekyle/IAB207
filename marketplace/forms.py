
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, IntegerField, BooleanField, SelectField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired


#creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name.'), Length(min=1, max=30, message="Max length of 30 characters")])
    password = PasswordField("Password", validators=[InputRequired('Enter user password.'), Length(min=1, max=30, message="Max length of 30 characters")])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired(), Length(min=1, max=30, message="Max length of 30 characters")])
    email_id = StringField("Email Address", validators=[Email("Enter a valid email."), Length(min=1, max=30, message="Max length of 30 characters")])

    #must be string field to not get rid of zero at the start, and allow for spaces
    phone = StringField("Phone Number", validators=[InputRequired("Enter a phone number."), Length(min=1, max=20, message="Max length of 20 numbers")])
    bankdetails = StringField("Bank Details (Only required if registering as a seller.)", validators=[Length(max=30, message="Max length of 30 numbers")])

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
    stock = IntegerField("Monthly Stock", validators=[InputRequired()])

    #categories for selector. Must be declared in tuples
    category = SelectField("Category", choices=[('Teddy Bears','Teddy Bears'), ('Farm Animals','Farm Animals'), ('Cats & Dogs','Cats & Dogs'), ('Wild Animals','Wild Animals'), ('Water Creatures','Water Creatures'), ('Other','Other')])
    
    #accepts up to 2 decimal places with regex validator
    price = StringField("Price ($$.cc)", validators=[InputRequired(), Regexp('^[0-9]+(\.[0-9]{1,2})?$', message="Not a valid decimal input ($$.cc)")])

    #name and desc with a max character length matching the db
    name = StringField("Product Name", validators=[InputRequired(), Length(min=1, max=500, message="Max length of 100 characters")])
    description = TextAreaField("Description", validators=[InputRequired(), Length(min=1, max=500, message="Max length of 500 characters")])

    #only the primary should be required while the others are optional
    image_one = FileField("Primary Image", validators=[FileRequired(), FileAllowed(ALLOWED_FILE, message="Only support jpg, JPG, png, PNG, bmp")])
    image_two = FileField("Second Image", validators=[FileAllowed(ALLOWED_FILE, message="Only support jpg, JPG, png, PNG, bmp")])
    image_three = FileField("Third Image", validators=[FileAllowed(ALLOWED_FILE, message="Only support jpg, JPG, png, PNG, bmp")])

    submit = SubmitField("Confirm")

#this is the post review form
class ReviewForm(FlaskForm):
    #review message, not required, can be empty
    text = TextAreaField("REVIEW", validators=[Length(min=0, max=500, message="Max length of 500 characters")])

    #rating options for selector, in tuples
    rating = SelectField("RATING", choices=[('1','1 Star'), ('2','2 Stars'), ('3','3 Stars'), ('4','4 Stars'), ('5','5 Stars')])

    title = StringField("TITLE", validators=[InputRequired(), Length(min=1, max=100, message="Max length of 100 characters")])

    submit = SubmitField("Post")


#this is the order form
class OrderForm(FlaskForm):
    #max quantity must be less than stock, otherwise error
    quantity = IntegerField("Quantity", validators=[InputRequired('Enter a quantity.')])
    
    #two of each because requires label and value
    state = SelectField("State", choices=[('QLD', 'QLD'), ('NSW', 'NSW'), ('VIC', 'VIC'), ('WA', 'WA'), ('SA', 'SA'), ('TAS', 'TAS'), ('NT', 'NT'), ('ACT', 'ACT')])
    
    city = StringField("City or Suburb", validators=[InputRequired('Enter a city or suburb.'), Length(min=1, max=100, message="Max length of 100 characters")])
    postcode = IntegerField("Postcode", validators=[InputRequired('Enter a postcode.')])
    address = StringField("Address", validators=[InputRequired('Enter an address.'), Length(min=1, max=100, message="Max length of 100 characters")])
    addinfo = TextAreaField("Additional Information", validators=[Length(min=0, max=500, message="Max length of 500 characters")])
    submit = SubmitField("Confirm Order")