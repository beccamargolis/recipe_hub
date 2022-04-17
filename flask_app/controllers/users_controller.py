from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.users_model import User
from flask_app.models.recipes_model import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():
    email_data = {'email': request.form['email']}
    user_in_db = User.get_by_email(email_data)
    if user_in_db:
        flash("Email already in use, please enter another.", 'register')
        return redirect('/')
    if not User.validate_register(request.form):
        return redirect('/')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    recipes = Recipe.get_user_recipes(data)
    return render_template("dashboard.html", user=user,recipes=recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')