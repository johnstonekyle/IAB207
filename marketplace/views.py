from flask import Blueprint, render_template, request
from .models import Product
import os
from . import db
import math
from sqlalchemy import and_, or_

bp = Blueprint('main', __name__,)

@bp.route('/', methods=['GET'])
def index():
    product_list = Product.query.order_by(Product.created).all()
    total_results = len(product_list)

    if (not product_list): #if no products exist then return 404
        return render_template('404.html')

    product_list = refine(product_list)

    return render_template('index.html',
        products = product_list,
        order = "Latest",
        category = "All Products",
        #caluclate max price
        max_price = find_max(product_list), 
        actual_max_price=find_max(product_list),
        #calculate number of results
        actual_results = len(product_list),
        total_results = len(product_list))



@bp.route('/<category>', methods=['GET'])
def index_category(category):

    product_list = Product.query.filter_by(category=category).order_by(Product.created).all()
    total_results = len(product_list)

    if (not product_list): #if no products exist then return 404
        return render_template('404.html')
    
    product_list = refine(product_list)

    return render_template('index.html',
        products = product_list,
        order = "Latest",
        category = category,
        #caluclate max price
        max_price = find_max(product_list),
        actual_max_price=find_max(product_list),
        #calculate number of results
        actual_results = len(product_list),
        total_results = len(product_list))



#produces a filtered list of results
@bp.route('/filter', methods = ['POST', 'GET'])
def filter():
    #initiate variables
    rating_min = 0
    price_max = 0
    search = ""
    order_dict = {
        "Latest": Product.created,
        "Least Expensive": Product.price,
        "Most Expensive": Product.price.desc(),
        "Alphabetical": Product.name,
    }

    #get result of all products
    complete_product_list = refine(Product.query.order_by(Product.created).all())

    if request.method == 'POST':
        rating_min = request.form['rating']
        price_max = request.form['pricerange']
        user_category = request.form['category']
        search = request.form['search']
        order = request.form['order']

   
    #if category is all, ignore category case
    if user_category == "All Products":
        product_list = Product.query.filter(and_(price_max>=Product.price,
            or_(Product.name.like("%" + search + "%"),
            Product.description.like("%" + search + "%")),
            )).order_by(order_dict[order]).all()
    
    else:
        product_list = Product.query.filter(and_(Product.price <=price_max,
            Product.category == user_category,
            or_(Product.name.like(search), 
            Product.description.like("%" + search + "%")),
            )).order_by(order_dict[order]).all()

    if (not product_list): #if no products exist then return 404
        return render_template('404.html')
    else:
        #refine the data within the given result
        product_list = refine(product_list)

    return render_template('index.html',
        user_search = search,
        products = product_list,
        order = order,
        category = user_category,
        #calculate max price
        max_price = price_max, #user specified
        actual_max_price=find_max(complete_product_list),
        #calculate number of results
        actual_results = len(complete_product_list),
        total_results = len(product_list))
   

#Custom Functions

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


#identifies max value in list of products
def find_max(result):
    max_value = 0  #initialise maximum value
    current_value = 0
    for product in result:
        current_value = round(5 * (math.ceil(product.price / 5)), 0) #round up to next 5
        if current_value > max_value:
            max_value = current_value
    
    return max_value