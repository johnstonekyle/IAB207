from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Product, User, Order
from .forms import OrderForm
from werkzeug.utils import secure_filename
import os
from . import db

bp = Blueprint('order', __name__, url_prefix='/order')


@bp.route("/<id>", methods=["GET", "POST"])
@login_required
def order(id):
    #check if user is a buyer
    if(current_user.seller):
        return redirect(url_for('product.view', id=id))

    order = OrderForm()
    if (order.validate_on_submit()):
        
        product = Product.query.filter_by(id=id).first()
        #retrieve information from the form
        quantity = order.quantity.data
        state = order.state.data
        city = order.city.data
        postcode = order.postcode.data
        address = order.address.data
        addinfo = order.addinfo.data
        fullAddress = "{}, {}, {}, {}".format(address, city, postcode, state)
        totalcost = (order.quantity.data * product.price)

        #check if ordered quantity is less than current stock
        if (quantity > product.current_stock):
            #if it is not, throw error
            flash("Sorry, you can currently order only " + str(product.current_stock) + " units of this item.")
            return redirect(url_for("order.order", id=product.id))
            
        else:
            #if it is, reduce current stock by amount purchased
            product.current_stock = (product.current_stock - quantity)
        
        
        new_order = Order(address=fullAddress, quantity=quantity, total_cost=totalcost, buyer_id=current_user.id, product_id=id)
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for("order.confirmation", id=new_order.id))

    else:
        # if validation fails, flash form errors
        for field, errors in order.errors.items():
            for error in errors:
                flash(u"%s: %s" % (getattr(order, field).label.text.title(), error), 'error')

        return render_template("order.html", form=order, heading="Order Confirmation")

@bp.route("/confirm<id>", methods=["GET", "POST"])
@login_required #would be better to specify must logged in as a buyer
def confirmation(id):
    
    #get order information
    order = Order.query.filter_by(id=id).first()

    #get product information
    product = Product.query.filter_by(id=order.product_id).first()

    return render_template("confirmation.html", data=order, extra_data=product, heading="Your Order")