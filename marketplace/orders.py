from flask import Blueprint, render_template

bp = Blueprint('order', __name__, url_prefix='/order')


@bp.route('/<id>', methods=['GET', 'POST'])
def order(id):
    return render_template('order.html')