from flask import Blueprint, render_template

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('/<id>')
def view(id):
    return render_template('product.html')

@bp.route('/add', methods=['GET', 'POST'])
def add():
    return render_template('add-product.html')