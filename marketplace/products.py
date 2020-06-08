from flask import Blueprint, render_template
from flask_login import login_required
from .models import Product, User

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('/<id>')
def view(id):
    product = Product.query.filter_by(id=id).first()
    if (not product): #if product doesnt exist then 404
        return render_template('404.html')

    #round price to 2 decimal places
    roundedPrice = round(product.price, 2)
    
    #get review rating average
    rating = 0
    index = 0
    for comment in product.comments:
        rating += comment.rating
        index += 1
    rating = round(rating/index, 2)

    #get seller info
    seller = User.query.filter_by(id=product.seller_id).first()

    return render_template('product.html', product=product, roundedPrice = roundedPrice, rating=rating, reviewCount=index, seller=seller)


@bp.route('/add', methods=['GET', 'POST'])
@login_required #would be better to specify must logged in as a seller
def add():
    return render_template('add-product.html')