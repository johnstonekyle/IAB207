from flask import Blueprint, render_template
from .models import Product
import os
from . import db

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET'])
def index():
    product_list = Product.query.order_by(Product.created).all()
    
    if (not product_list): #if no products exist then return 404
        return render_template('404.html')

    #round price to 2 decimal places
    for product in product_list:
        product.price = round(product.price, 2)
    
        #get review rating average
        product.rating = 0
        i = 0
        for comment in product.comments:
            product.rating += comment.rating
            i += 1
        if i > 0:
            product.rating = round(product.rating/i, 1)
        else:
            product.rating = 'N/A'

    return render_template('index.html', products = product_list)

