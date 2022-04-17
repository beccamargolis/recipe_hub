from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db_name = 'recipes_schema'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.instructions = db_data['instructions']
        self.under_thirty = db_data['under_thirty']
        self.date_made = db_data['date_made']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    

    @classmethod
    def save_recipe(cls,data):
        query = "INSERT INTO recipes (user_id,name,description,instructions,under_thirty,date_made) VALUES (%(user_id)s,%(name)s,%(description)s,%(instructions)s,%(under_thirty)s,%(date_made)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_user_recipes(cls,data):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under_thirty=%(under_thirty)s, date_made=%(date_made)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
            query = "DELETE FROM recipes WHERE recipes.id = %(id)s;"
            return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters.","recipe")
        if len(recipe['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters.","recipe")
        if len(recipe['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters.","recipe")
        if (recipe['date_made']) == "":
            is_valid = False
            flash("Date must be provided.", "recipe")

        return is_valid