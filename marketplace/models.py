from . import db
from datetime import datetime
from flask_login import UserMixin

class Product(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    current_stock = db.Column(db.Integer, nullable=False)
    monthly_stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    image_one = db.Column(db.String(400))
    image_two = db.Column(db.String(400))
    image_three = db.Column(db.String(400))

    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments = db.relationship('Comment', backref='product') #comments on product

    def __repr__(self):
        return "<product: {}>".format(self.name)


class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(500))
    rating = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    def __repr__(self):
        return "<comment: {}>".format(self.text)


class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(500), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Numeric, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    def __repr__(self):
        return "<order: {}>".format(self.id)


class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), index=True, unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False) #must be string to keep 0 at start of number
    bank_account = db.Column(db.String(30))
    seller = db.Column(db.Boolean, nullable=False) #determines whether the user is a seller or buyer
    password_hash = db.Column(db.String(255), nullable=False)

    products = db.relationship('Product', backref='user') #products added by user

    def __repr__(self):
        return "<user: {}>".format(self.username)

