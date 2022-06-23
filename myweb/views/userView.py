import functools
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session, g
from myweb.models.User import User
from werkzeug.security import generate_password_hash, check_password_hash
from myweb import db

userView = Blueprint('user',__name__,url_prefix='/user')

#Registro de usuario
@userView.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        error = None
        if len(username) < 3:
            error = 'El nombre de usuario debe tener al menos 3 caracteres'
            flash(error)
        if len(password) < 6:
            error = 'La contraseña debe tener al menos 6 caracteres'
            flash(error)
        if password != confirm_password:
            error = 'Las contraseñas no coinciden'
            flash(error)
        
        user_name = User.query.filter_by(username=username).first()
        
        if user_name == None:
            user = User(username, generate_password_hash(password)) #Crear usuario
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
        else:
            error = 'El nombre de usuario ya existe'
            flash(error)
            
    return render_template('user/register.html')


#Login de usuario
@userView.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not username:
            error = 'El nombre de usuario es requerido'
            flash(error)
        elif not password:
            error = 'La contraseña es requerido'
            flash(error)
        elif user == None:
            error = 'El nombre de usuario no existe'
            flash(error)
        elif not check_password_hash(user.password, password):
            error = 'La contraseña es incorrecta'
            flash(error)
        elif user and check_password_hash(user.password, password):
            session.clear()
            session['user_id'] = user.id
            session['user_name'] = user.username
            return redirect(url_for('index'))
        else:
            error = 'Usuario o contraseña incorrecto'
            flash(error)
    return render_template('user/login.html')

#Verificar si el usuario esta logueado
@userView.before_app_request
def load_logged_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

#Logout de usuario
@userView.route('/logout')
def logout():
    session.clear()
    g.user = None
    return redirect(url_for('index'))


#Verificar si el usuario es requerido para acceder a las rutas
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))
        return view(**kwargs)
    return wrapped_view