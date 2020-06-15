from flask import Blueprint, render_template
from .models import Product
import os
from . import db

bp = Blueprint('main', __name__,)

order_options = ["Product.created", "Product.price", "Product.price.desc", "Product.product"]


@bp.route('/', methods=['GET'])
def index():
    product_list = Product.query.order_by(Product.created).all()
    total_results = len(product_list)

    if (not product_list): #if no products exist then return 404
        return render_template('404.html')

    return render_template('index.html', products = refine(product_list), category = "All Products", max_price=find_max(product_list), total_results = total_results)

@bp.route('/<category>', methods=['GET'])
def index_category(category):

    product_list = Product.query.filter_by(category=category).order_by(Product.created).all()
    total_results = len(product_list)

    if (not product_list): #if no products exist then return 404
        return render_template('404.html')

    return render_template('index.html', products = refine(product_list), category = category, max_price=find_max(product_list), total_results = total_results)

#user query
def user_query():
    product_list = Product.query.order_by(Product.created).all()
    if (not product_list): #if no products exist then return 404
        return render_template('404.html')

    return render_template('index.html', products = refine(product_list))

##Function which analyses and refines all data gathered for users 
def refine(result): 
    #round price to 2 decimal places
    for product in result:
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

    return result

def find_max(result):
    max_value = 0  #initialise maximum value
    for product in result:
        product.price = round(product.price)
        if product.price > max_value:
            max_value = product.price
    
    return max_value
