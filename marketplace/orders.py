from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('order', __name__, url_prefix='/order')


@bp.route('/<id>', methods=['GET', 'POST'])
@login_required #would be better to specify must logged in as a buyer
def order(id):
    return render_template('order.html')