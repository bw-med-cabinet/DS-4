# app/routes/flask_app.py

#> import packages
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from flask_cors import cross_origin
from app.models import Cannabis, db, parse_records

import json


home_routes = Blueprint("home_routes", __name__)


@home_routes.route("/")
def index(): # <prod>
    return redirect("/home")


@home_routes.route("/home")
def home(): # <prod>
    return render_template("home.html")


@home_routes.route("/about")
def about(): # <prod>
    return render_template("about.html")


@home_routes.route("/cannabis")
def cannabis(): # <prod>
    """database endpoint. 

    Returns:
        dictionary (json object)
    """
    db_cannabis = Cannabis.query.all()
    cannabis_response = parse_records(db_cannabis)
    return jsonify(cannabis_response)


@home_routes.route("/dev/cross_route", methods=['GET', 'POST'])
@cross_origin()
def cross_api(): # <dev>
    """cross origin requests developement route.
    
    Used for testing incoming requests from different URIs. 
    
    Returns:
        dictionary (json object)
    """
    return jsonify({'data': 'The text is being displayed!'})


