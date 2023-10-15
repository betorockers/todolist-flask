# ACA IRAN LAS AUTENTICACIONES #
from flask import (Blueprint, render_template, request, url_for, redirect, flash, session, g)
#! importamos (generate_password_hash y check_password_hash) para encriptar nuestras pass y tambien para chequear nuestros datos
from werkzeug.security import generate_password_hash, check_password_hash
#! importamos User y la base de datos
from .models import User
from todor import db

#! importamos la base de datos
#from . import models

#! ruta inicial con url_prefix
bp = Blueprint('auth', __name__, url_prefix='/auth')

#! registramos usuario en nuestra base de datos
@bp.route('/register', methods = ('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User(username, generate_password_hash(password))
        
        #* creamos la variable error
        error = None
        
        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El usuario {username} ya esta registrado'
            
        flash(error)
    
    return render_template('auth/register.html')

#! aca autenticaremos la iniio de sesion
@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        error = None
        
        #*validar datos        
        user = User.query.filter_by(username = username).first()
        if user == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'Contraseña incorrecta'
        
        #* Iniciar sesion 
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('todo.index'))
                    
        flash(error)
    return render_template('auth/login.html')

#* funcion para mantener la sesion iniciada
@bp.before_app_request
def load_logger_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)
        
#! creamos la vista logout(cerrar sesion)
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#! crearemos la funcion requerir autenticacion
import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view