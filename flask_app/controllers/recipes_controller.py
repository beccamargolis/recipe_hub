from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.users_model import User
from flask_app.models.recipes_model import Recipe



@app.route('/new/recipe') # to show the create recipe page
def new():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template("create.html", user=User.get_by_id(data))

@app.route('/create/recipe', methods=['POST']) # to actually create a new user and redirect back to home; POST method because data is being submitted
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_thirty": int(request.form["under_thirty"]),
        "date_made": request.form["date_made"],
        "user_id": session['user_id']
    }
    Recipe.save_recipe(data)
    return redirect('/dashboard')

@app.route('/view/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("view_recipe.html",recipe=Recipe.get_one(data),user=User.get_by_id(user_data))

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_recipe.html",edit=Recipe.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/recipe',methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/dashboard')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_thirty": int(request.form["under_thirty"]),
        "date_made": request.form["date_made"],
        "id": request.form["id"]
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/destroy/recipe/<int:id>')
def destroy_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')