from enum import unique

from sqlalchemy.orm import relationship
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True)
    password = db.Column(db.String(150))
    recipes = db.relationship('Recipe')
    favorites = db.relationship('Favorite')


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipeName = db.Column(db.String(10000), unique=True)
    meat = db.Column(db.String(10000))
    totalTime = db.Column(db.String(10000))
    preparation = db.Column(db.String(10000))
    instructions = db.Column(db.String(10000))
    imgName = db.Column(db.String(100), unique=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    favorites = db.relationship('Favorite')


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipeName = db.Column(db.String(10000))
    meat = db.Column(db.String(10000))
    totalTime = db.Column(db.String(10000))
    preparation = db.Column(db.String(10000))
    instructions = db.Column(db.String(10000))
    imgName = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
