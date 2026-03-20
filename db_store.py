from flask import session
import pymysql.cursors
from  datetime import datetime


def get_db():
    db = pymysql.connect(
        host='localhost',
        user='a22304873',
        password='f0781e',
        database='db_a22304873',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    return db




def get_products(limit,offset):
    db = get_db().cursor()
    query = 'SELECT * FROM products LIMIT %s offset %s'
    db.execute(query,(limit,offset))
    products = db.fetchall()
    return products
def count_products():
    db = get_db().cursor()
    query = 'SELECT COUNT(*) FROM products'
    db.execute(query)
    count=db.fetchone()
    return count['COUNT(*)']

def get_categories():
    db = get_db().cursor()
    query = 'SELECT * FROM categories'
    db.execute(query)
    categories = db.fetchall()
    return categories

def get_product_category(product_id):
    db = get_db().cursor()
    query = 'SELECT cat_id FROM products where id = %s'
    db.execute(query, (product_id,))
    cat_id = db.fetchone()
    query_category="SELECT name FROM categories where id = %s"
    db.execute(query_category, (cat_id['cat_id'],))
    category = db.fetchone()
    return category['name']
def get_orders(customer_id):
    db = get_db().cursor()
    query = 'SELECT * FROM orders where customer_id = %s'
    db.execute(query,(customer_id,))
    orders = db.fetchall()
    return orders

def get_order_details(order_id):
    db = get_db().cursor()
    query = "SELECT * FROM order_items left join products as p on order_items.product_id= p.id where order_items.order_id = %s"
    db.execute(query, (order_id,))
    order_details = db.fetchall()
    return order_details

def get_order_items(order_id):
    db = get_db().cursor()
    query = 'SELECT * FROM order_items where order_id = %s'
    db.execute(query,(order_id,))
    order_items = db.fetchone()
    return order_items

def get_product(product_id):
    db = get_db().cursor()
    query = 'SELECT * FROM products where id = %s'
    db.execute(query, (product_id,))
    product = db.fetchone()
    return product

def create_order(total):
    query = "Insert into orders(customer_id,created_at,status,total) values (%s,%s,%s,%s)"
    db = get_db()
    cur=db.cursor()
    cur.execute(query=query, args=(session['user_id'],datetime.now(),0,total,))
    db.commit()
    return cur.lastrowid


def insert_order_item(last_order,product_id, item_quantity):
    query = "Insert into order_items(order_id,product_id,quantity) values (%s,%s,%s)"
    db = get_db()
    cur = db.cursor()
    cur.execute(query=query, args=(last_order,product_id,item_quantity,))
    db.commit()

def basket_status():
    db = get_db().cursor()    
    total = 0
    quantity = 0 
    basket = session['basket']
    for key, value in basket.items():
        quantity += value
        query = "select * from products where id='" + str(key) + "'"
        db.execute(query)
        product = db.fetchone()
        total += value * product['price']
    return {'quantity': quantity, 'total': total}

def get_basket_products():
    pass

    


