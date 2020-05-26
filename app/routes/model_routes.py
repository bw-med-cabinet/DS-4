#> app/routes/model_app.py

#> import packages
from flask import Blueprint, jsonify, request, render_template
from app.models import Cannabis, db, parse_records


import pickle
import numpy
import json
import pandas as pd


model_routes = Blueprint("model_routes", __name__)


# Open pickle with trained model
    

@model_routes.route("/cannabis")
def cannabis():
    """database endpoint.

    Returns:
        dictionary (json object)
    """
    db_cannabis_model = Cannabis.query.all()
    cannabis_response = parse_records(db_cannabis_model)
    return jsonify(cannabis_response)


@model_routes.route("/knn_model", methods=['GET', 'POST'])
def knn_model_recommender():
    """creates list with top n recommended strains.

    Paramaters:
        request: dictionary (json object)
            list of user's strain description

        n: int, optional
            number of recommendations to return, default 5.

    Returns:
        list_model_id: python list of n recommended strains.
    """
    user_dictionary = request.json
    n = 5
    
    """
    Model
    """
    
    data = numpy.array(vector)
    request_array = pd.Series(data, index=columns)
    _, neighbors = nn.kneighbors([request_series])

    list_strains = []
    for points in neighbors:
        for index in points:
            list_strains.append(index)
    
    return_list = [
    str(val)
    for val in list_model_id[:n]
    ]
    
    records = parse_records(Cannabis.query.filter(Cannabis.model_id.in_(return_list)).all())
    
    return jsonify(records)
    