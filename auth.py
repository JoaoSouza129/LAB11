import hashlib
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, make_response
)


from LAB11.db_auth import (
    register_user,login_user, generate_cookie,cookie_reset,validate_email
)

from LAB11.db_store import basket_status

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        confirmPassword=request.form['confirmPassword']

        error=None
        emailValido=validate_email(email)
        if username is None or email is None or password is None or confirmPassword is None:
            error="Todos os campos devem ser preenchidos"
        elif password != confirmPassword:
            error="passwords não coincidem" 
        elif emailValido is False:
            error="Email Inválido"

        

        if error==None:
            error=register_user(username,email,password)
        
        if error==None:
            return redirect(url_for("auth.login"))

        flash(error)
    tamanho_carrinho = 0
    basket = session.get('basket')
    tamanho_carrinho = 0
    if basket is not None:
        tamanho_carrinho = len(basket)
    return render_template("auth/register.html",tamanho_carrinho=tamanho_carrinho)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        rememberMe=request.form.get('rememberME')
        basket = session.get('basket')
        error=None
        user=login_user(email,password)
        if user is None or user['password_digest'] != hashlib.md5(str(password).encode()).hexdigest():
            error="email or password incorrect"
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username']=user['name']
            session['basket']=basket
            session.modified=True
            message="Welcome Back "+session['username']
            resposta=make_response(render_template("shop/message.html",message=message,basket=basket))
            if rememberMe !=None:
                cookie = generate_cookie(email)
                resposta.set_cookie('remember_me', cookie,1296000)
                
            return resposta 
        flash(error)
    basket=session.get('basket')
    tamanho_carrinho=0
    if basket is not None:
        tamanho_carrinho = len(basket)
    return render_template("auth/login.html",tamanho_carrinho=tamanho_carrinho)

@bp.route('/logout')
def logout():
    cookie_reset(session['user_id'])
    session.clear()
    message="See you soon"
    resp = make_response(render_template('shop/message.html',message=message))
    resp.set_cookie('remember_me', '', expires=0)
    return resp    



