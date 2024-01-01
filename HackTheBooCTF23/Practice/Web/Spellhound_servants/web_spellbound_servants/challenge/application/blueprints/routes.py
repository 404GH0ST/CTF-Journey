from application.database import *
from flask import Blueprint, redirect, render_template, request, make_response
from application.util import response, isAuthenticated

web = Blueprint('web', __name__)
api = Blueprint('api', __name__)

@web.route('/', methods=['GET', 'POST'])
def loginView():
    return render_template('login.html')

@web.route('/register', methods=['GET', 'POST'])
def registerView():
    return render_template('register.html')

@web.route('/home', methods=['GET', 'POST'])
@isAuthenticated
def homeView(user):
    return render_template('index.html', user=user)

@api.route('/login', methods=['POST'])
def api_login():
    if not request.is_json:
        return response('Invalid JSON!'), 400
    
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    if not username or not password:
        return response('All fields are required!'), 401
    
    user = login_user_db(username, password)
    
    if user:
        res = make_response(response('Logged In sucessfully'))
        res.set_cookie('auth', user)
        return res
        
    return response('Invalid credentials!'), 403

@api.route('/register', methods=['POST'])
def api_register():
    if not request.is_json:
        return response('Invalid JSON!'), 400
    
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    if not username or not password:
        return response('All fields are required!'), 401
    
    user = register_user_db(username, password)
    
    if user:
        return response('User registered! Please login'), 200
        
    return response('User already exists!'), 403
