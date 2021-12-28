import os
from flask import Blueprint, app, render_template, request, flash, jsonify
from flask.helpers import url_for
from flask_login import login_required, current_user
from .models import Recipe, Favorite
from . import db
import json
import uuid


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():

    return render_template("home.html", user=current_user)


@views.route('/library', methods=['GET', 'POST'])
@login_required
def library():

    recipes = Recipe.query.order_by(Recipe.recipeName)
    favorites = Favorite.query.order_by(Favorite.recipeName)

    return render_template("library.html", user=current_user, recipes=recipes, favorites=favorites)


@views.route('/createNew', methods=['GET', 'POST'])
@login_required
def createNew():
    if request.method == 'POST':
        recipeName = request.form.get('recipeName')
        meat = request.form.get('meat')
        totalTime = request.form.get('totalTime')
        preparation = request.form.get('preparation')
        instructions = request.form.get('instructions')

        imgName = str(uuid.uuid1()) + \
            os.path.splitext(request.files['img'].filename)[1]
        request.files['img'].save(os.path.join(
            'package/static/userImages', imgName))

        if len(recipeName) < 1:
            flash('Recipe is too short!', category='error')
        else:
            new_recipe = Recipe(recipeName=recipeName, meat=meat, totalTime=totalTime,
                                preparation=preparation, instructions=instructions, imgName=imgName,  user_id=current_user.id)
            db.session.add(new_recipe)
            db.session.commit()

            flash('Recipe added!', category='success')

    return render_template("createNew.html", user=current_user)


@views.route('/favorites', methods=['GET', 'POST'])
@login_required
def favorite():

    favorite = Favorite.query.order_by(Favorite.recipeName)

    return render_template("favorites.html", user=current_user, favorite=favorite)


@views.route('/recipe/<recipeId>', methods=['GET', 'POST'])
def goto_recipe(recipeId):

    recipe = Recipe.query.get(recipeId)
    img = url_for('static', filename='userImages/' + Recipe.imgName)

    return render_template("recipe.html", user=current_user, recipe=recipe, img=img)


@views.route('/delete-recipe', methods=['POST'])
@login_required
def delete_recipe():
    recipe = json.loads(request.data)
    recipeId = recipe['recipeId']
    recipe = Recipe.query.get(recipeId)
    if recipe:
        if recipe.user_id == current_user.id:
            db.session.delete(recipe)
            db.session.commit()
            flash('Recipe deleted!', category='success')

    return jsonify({})


@views.route('/add-favorite', methods=['GET', 'POST'])
@login_required
def add_favorite():
    recipe = json.loads(request.data)
    recipeId = recipe['recipeId']
    recipe = Recipe.query.get(recipeId)

    if recipe:
        if recipe.id == recipe.id:
            addFavorite = Favorite(recipe_id=recipe.id, recipeName=recipe.recipeName, meat=recipe.meat, totalTime=recipe.totalTime,
                                   preparation=recipe.preparation, instructions=recipe.instructions, imgName=recipe.imgName, user_id=current_user.id)

            db.session.add(addFavorite)
            db.session.commit()
            flash('recipe added to your locker')

    return render_template("library.html", user=current_user,)


@views.route('/delete-favorite', methods=['POST'])
@login_required
def delete_favorite():
    favorite = json.loads(request.data)
    favoriteId = favorite['favoriteId']
    favorite = Favorite.query.get(favoriteId)

    if favorite:
        if favorite.user_id == current_user.id:
            db.session.delete(favorite)
            db.session.commit()
            flash('deleted from favorites!', category='success')

    return jsonify({})
