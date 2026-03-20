import math

import flask
from flask import (
    Blueprint, render_template, session, redirect, url_for, request, flash
)

from LAB11.db_store import (
    get_categories, get_products, get_orders, get_order_details,
    get_order_items, create_order, get_product, insert_order_item, basket_status, get_basket_products,
    get_product_category, count_products
)
from LAB11.db_auth import (
    validate_cookie
)
from pyexpat.errors import messages

bp = Blueprint('store', __name__)


@bp.route('/')
def index():
    lab_name = 'LAB11'
    page = request.args.get('page', 1, type=int)
    PER_PAGE = 8
    offset = (page - 1) * PER_PAGE
    total_pages = math.ceil(count_products() / PER_PAGE)
    tamanho = 0
    products = get_products(limit=PER_PAGE, offset=offset)

    carrinho = session.get('basket')
    if carrinho is not None:
        tamanho = len(carrinho)
    user = None

    if 'user_id' not in session:
        remember_me = request.cookies.get('remember_me')
        if remember_me:
            user = validate_cookie(remember_me)
            if user:
                session.clear()
                session['user_id'] = user['id']
                session['username'] = user['name']
    return render_template('shop/index.html', lab_name=lab_name, products=products, tamanho=tamanho, page=page,
                           total_pages=total_pages)


@bp.route('/products')
@bp.route('/products/<int:id>')
def products(id=None):
    pass


@bp.route('/checkout')
def checkout():
    global tamanho_carrinho
    if request.method == 'GET':
        itens_do_carrinho = []
        valor_total = 0
        carrinho = session.get('basket')
        if carrinho is not None:
            for id, quantity in session['basket'].items():
                product = get_product(id)
                category = get_product_category(id)
                subtotal = get_product(id)['price'] * quantity
                valor_total = valor_total + subtotal
                temp_infos = {
                    'id': product['id'],
                    'name': product['name'],
                    'price': product['price'],
                    'image': product['image'],
                    'category': category,
                    'quantity': quantity,
                    'subtotal': subtotal,
                    'valor_total': valor_total
                }
                itens_do_carrinho.append(temp_infos)

            tamanho_carrinho = len(itens_do_carrinho)

            return render_template('shop/checkout.html', itens_do_carrinho=itens_do_carrinho, valor_total=valor_total,
                                   tamanho_carrinho=tamanho_carrinho)
        else:
            return render_template('shop/checkout.html', valor_total=valor_total, carrinho=carrinho)


@bp.route('/order', methods=['GET', 'POST'])
def order():
    basket = session.get('basket')
    user_id = session.get('user_id')
    tamanho_carrinho = 0
    if basket is not None:
        tamanho_carrinho = len(basket)
    if user_id is None:
        return redirect(url_for('auth.login', tamanho_carrinho=tamanho_carrinho))
    if not basket:
        message = "Carrinho vazio, adicione itens ao carrinho para realizar checkout"
        flask.flash(message)
        return redirect(url_for('store.index'))
    if request.method == 'POST':
        total = 0
        for id, quantity in session['basket'].items():
            subtotal = get_product(id)['price'] * quantity
            total = total + subtotal
        order_id = create_order(total)
        for id, quantity in session['basket'].items():
            insert_order_item(order_id, id, quantity)
        session.pop('basket')
        return redirect(url_for('store.orders'))


@bp.route('/orders')
def orders():
    user_id = session.get('user_id')
    basket = session.get('basket')
    tamanho_carrinho = 0
    if basket is not None:
        tamanho_carrinho = len(basket)
    orders = get_orders(user_id)

    return render_template('shop/orders.html', orders=orders, tamanho_carrinho=tamanho_carrinho)


@bp.route('/add/<int:id>')
def add_basket(id):
    id_item = str(id)
    basket = session.get('basket')
    if basket is None:
        basket = {}
    if id_item in basket:
        basket[id_item] += 1
    else:
        basket[id_item] = 1
    session['basket'] = basket
    session.modified = True
    return redirect(url_for('store.index'))


@bp.route('/empty')
def empty_basket():
    basket = session.get('basket')

    session.pop('basket', None)
    return redirect(url_for('store.index'))


@bp.route('/remove/<int:id>')
def remove(id):
    product_id = str(id)
    basket = session.get('basket')
    if basket is None:
        return redirect(url_for('store.checkout'))

    basket.pop(product_id, None)
    session['basket'] = basket
    session.modified = True
    return redirect(url_for('store.checkout'))


@bp.route('/decrement/<int:id>')
def decrement(id):
    product_id = str(id)
    basket = session.get('basket')
    if basket is None:
        return redirect(url_for('store.checkout'))

    basket[product_id] -= 1
    if basket[product_id] == 0:
        basket.pop(product_id, None)
    session['basket'] = basket
    session.modified = True
    return redirect(url_for('store.checkout'))


@bp.route('/increment/<int:id>')
def increment(id):
    product_id = str(id)
    basket = session.get('basket')
    if basket is None:
        return redirect(url_for('store.checkout'))

    basket[product_id] += 1
    if basket[product_id] == 0:
        basket.pop(product_id, None)
    session['basket'] = basket
    session.modified = True
    return redirect(url_for('store.checkout'))


@bp.route('/order_details/<int:id>')
def order_details(id):
    order_details = get_order_details(id)
    return render_template("shop/order_details.html", order_details=order_details)
