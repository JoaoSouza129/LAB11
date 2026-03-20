from flask import session
import pymysql.cursors
import hashlib
from  datetime import datetime
import email_validator

def get_db():
    db = pymysql.connect(
        host='localhost',
        user='db_username',
        password='db_password',
        database='db_name',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    return db


def register_user(username, email, password):
    error=None
    try:
        query="Insert into customers(name,email,password_digest,created_at,updated_at) values (%s,%s,%s,NOW(),NOW())"
        db=get_db()
        db.cursor().execute(query=query,args=(username,email,hashlib.md5(str(password).encode()).hexdigest(),))
        db.commit()
    except db.IntegrityError:
       error=f"Email {email} is already registered."
    return error

def login_user(email,password):
    db=get_db().cursor()
    db.execute("SELECT * FROM customers WHERE email = %s", (email,))
    user=db.fetchone()
    return user




def generate_cookie(email):
    db = get_db()
    present_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    remember_digest = hashlib.md5(str(datetime.now()).encode()).hexdigest()

    query  = "UPDATE customers SET remember_digest = %s , updated_at =%s WHERE email = %s"
    db.cursor().execute(query, (remember_digest,present_date,email,)) 
    db.commit()
    return remember_digest

def validate_cookie(cookie):
    db = get_db().cursor()
    query = "SELECT * from customers where remember_digest=%s"
    db.execute(query,(cookie,))
    user = db.fetchone()
    return user

def cookie_reset(id):
    pass

def validate_email(email):
    try:
        email_validator.validate_email(email)
        valido=True
    except email_validator.EmailNotValidError:
        valido=False
    return valido
