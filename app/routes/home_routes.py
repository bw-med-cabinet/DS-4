# app/routes/flask_app.py

#> import packages
from flask import Blueprint, jsonify, request, render_template
from app.models import Cannabis, db, parse_records

import json


home_routes = Blueprint("home_routes", __name__)


@home_routes.route("/")
def home():
    hello = "Hello World!"
    return jsonify(hello)