from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('/<id>')
def view(id):
    return render_template('product.html')

@bp.route('/add', methods=['GET', 'POST'])
@login_required #would be better to specify must logged in as a seller
def add():
    return render_template('add-product.html')