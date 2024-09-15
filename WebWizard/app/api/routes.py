from flask import Blueprint, render_template, redirect, url_for, flash, make_response, session,current_app
from flask_jwt_extended import create_access_token, create_refresh_token    
from app.Models.models import User, Session, Contact
from app.Forms.forms import LoginForm, RegisterForm, ContactForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_user, logout_user, login_required

api_bp = Blueprint('api', __name__)

limiter = Limiter(key_func=get_remote_address, default_limits=["5 per minute"])

# This function will redirect the user to the login page
@api_bp.route('/', methods=['GET'])
def index():
    return render_template('WebWizard.html')

# This function and route is for the user to login 
@api_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def Login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Session.query(User).filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            current_app.logger.info(f"User {form.username.data} logged in successfully")

            session['user_id'] = user.id
            login_user(user)

            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            response = make_response(redirect(url_for('api.adds')))  
            response.set_cookie('access_token_cookie', access_token, httponly=True)
            response.set_cookie('refresh_token_cookie', refresh_token, httponly=True)

            return response 
        else:
            flash('Invalid username or password')
            current_app.logger.info(f"User {form.username.data} login unsuccessfully")

    return render_template('Login.html', form=form)


# This function and route is for the user to register
@api_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def Register():
    form = RegisterForm()

    # If the form is submitted and validated, the user will be redirected to the login page
    if form.validate_on_submit():
        passcode = generate_password_hash(form.password.data)  
        user = User(username=form.username.data, password=passcode)
        Session.add(user)
        Session.commit()
        flash('User created successfully')
        return redirect(url_for('api.Login'))
    else:
        Session.rollback()
        flash('User creation failed')
    return render_template('Register.html', form=form)

# This function and route is for the user to logout
@api_bp.route('/logout', methods=['GET'])  
@login_required
def Logout():

    response = make_response(redirect(url_for('api.index')))
    response.delete_cookie('access_token_cookie')  
    response.delete_cookie('refresh_token_cookie') 
    logout_user()
    session.clear()
    return response

@api_bp.route('/adds', methods=['GET', 'POST'])
@login_required
@limiter.limit("10 per minute")
def adds():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            user_id = session.get('user_id')
            contact = Contact(name=form.name.data, phone=form.phone.data, amount=form.amount.data ,user_id=user_id)
            Session.add(contact)  
            Session.commit() 
            current_app.logger.info(f"User {user_id} added a contact")
            flash('Registered successfully', 'success')
            return redirect(url_for('api.adds'))
        except:
            Session.rollback()
            flash('Failed to add', 'danger')
            return redirect(url_for('api.Login'))
    else:
        return render_template('Add.html', form=form)

