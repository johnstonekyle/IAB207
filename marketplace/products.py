from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Product, User, Comment
from .forms import AddProductForm
from werkzeug.utils import secure_filename
import os
from . import db

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
    i = 0
    for comment in product.comments:
        rating += comment.rating
        i += 1
    if i > 0:
        rating = round(rating/i, 2)
    else:
        rating = 'N/A'

    #get seller info
    seller = User.query.filter_by(id=product.seller_id).first()

    #get seller avg rating
    sellerRating = 0
    j = 0
    for prod in seller.products:
        for com in prod.comments:
            sellerRating += com.rating
            j += 1
    if j > 0:
        sellerRating = round(sellerRating/j, 2)
    else:
        sellerRating = 'N/A'

    #get comments with user joined
    comments = db.session.query(Comment, User).filter_by(product_id=id).outerjoin(User, Comment.user_id == User.id).all()

    return render_template('product.html', product=product, roundedPrice = roundedPrice, rating=rating, reviewCount=i, seller=seller, sellerRating=sellerRating, sellerReviewCount=j, comments=comments)

def check_upload_file(fp, filename):
    #filename = fp.filename

    #current relative base path
    BASE_PATH = os.path.dirname(__file__)
    #combined base path with image folder and file name
    upload_path = os.path.join(BASE_PATH, 'static/img/products', secure_filename(filename))
    #the path that will be stored and can be used in HTML
    dp_upload_path = '/static/img/products/'+ secure_filename(filename)

    fp.save(upload_path)
    return dp_upload_path

@bp.route('/add', methods=['GET', 'POST'])
@login_required #would be better to specify must logged in as a seller
def add():
    form = AddProductForm()

    if(form.validate_on_submit()):

        #get data from form
        f_stock = form.stock.data
        f_category = form.category.data
        f_price = form.price.data
        f_name = form.name.data
        f_description = form.description.data

        #check if product exists
        for product in current_user.products:
            if product.name == f_name:
                flash('This product already exists', 'error')
                return render_template('add-product.html', form=form)


        #save primary image and get path
        image_one_filename = "{}_{}_primary_{}".format(current_user.id, form.name.data, form.image_one.data.filename)
        image_one_path = check_upload_file(form.image_one.data, image_one_filename)

        #save second image and get path
        image_two_path = None
        if form.image_two.data != None:
            image_two_filename = "{}_{}_second_{}".format(current_user.id, form.name.data, form.image_two.data.filename)
            image_two_path = check_upload_file(form.image_two.data, image_two_filename)

        #save third image and get path
        image_three_path = None
        if form.image_three.data != None:
            image_three_filename = "{}_{}_third_{}".format(current_user.id, form.name.data, form.image_three.data.filename)
            image_three_path = check_upload_file(form.image_three.data, image_three_filename)

        #create new product object
        new_product = Product(
            name=f_name, 
            description=f_description, 
            current_stock=f_stock, 
            monthly_stock=f_stock, 
            price=f_price, 
            category=f_category, 
            image_one=image_one_path, 
            image_two=image_two_path, 
            image_three=image_three_path, 
            seller_id=current_user.id)
        
        #save new product to database
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('product.view', id=new_product.id))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"%s: %s" % (getattr(form, field).label.text.title(), error), 'error')

    return render_template('add-product.html', form=form)