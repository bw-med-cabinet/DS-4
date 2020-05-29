#> app/routes/model_app.py

#> import statements
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from flask_cors import cross_origin
from app.models import Cannabis, db, parse_records

import pickle
import numpy
import json
import pandas as pd

from sklearn.neighbors import NearestNeighbors


model_routes = Blueprint("model_routes", __name__)

#> Neural Nearest Neighbors Network <knn01>
knn01_dtm = pickle.load(open('./app/data/knn01_dtm.pkl', 'rb'))
knn01_tf = pickle.load(open('./app/data/knn01_tf.pkl', 'rb'))

knn01_nn = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
knn01_nn.fit(knn01_dtm)

#> Natural Language Processing Network <nlp01>
nlp01_dtm = pickle.load(open('./app/data/nlp01_dtm.pkl', 'rb'))
nlp01_tf = pickle.load(open('./app/data/nlp01_tf.pkl', 'rb'))

nlp01_nn = NearestNeighbors(n_neighbors=5, algorithm='brute')
nlp01_nn.fit(nlp01_dtm)


@model_routes.route("/cannabis/user_form")
def user_form_knn01(): # <prod>
    """recommender user choice form.

    Returns:
        request: dictionary (json object)
            list of user's strain description
            
        schema:
        {"type_list": [""],
        "effect_list": [""],
        "flavor_list": [""]}
    """
    return render_template("user_form.html")


@model_routes.route("/cannabis/user_form_text")
def user_form_nlp01(): # <prod>
    """recommender user text form.

    Returns:
        request: dictionary (json object)
            user's strain description
            
        schema:
        {"dict_list": [""]}
    """
    return render_template("user_form_text.html")


@model_routes.route("/cannabis/output_knn01", methods=['GET', 'POST'])
def knn01_model_recommender():
    """creates list with top n recommended strains. <prod>

    Paramaters:
        request: dictionary (json object)
            list of user's strain description

        n: int, optional
            number of recommendations to return, default 3.

    Returns:
        list_model_id: python list of n recommended strains.
    """
    
    type_list = request.form.get("type_list")
    effect_list = request.form.get("effect_list")
    flavor_list = request.form.get("flavor_list")	

    type_list, effect_list, flavor_list = (
        request.form.getlist("type_list"),
        request.form.getlist("effect_list"),
        request.form.getlist("flavor_list")
    )
    
    # MILESTONE 00 #> User request

    type_list = [type_list.lower() for type_list in type_list]
    effect_list = [effect_list.lower() for effect_list in effect_list]
    flavor_list = [flavor_list.lower() for flavor_list in flavor_list]

    request_text = [type_list,
                    effect_list, 
                    flavor_list                    
                ]
    
    result_text = [] # Merges input lists
    for sublist in request_text:
        for n in sublist:
            result_text.append(n)

    result_string = [' '.join(str(n) for n in result_text)] # Joins into a single string

    # MILESTONE 01 #> User request shown as list

    output_strain_dense = knn01_tf.transform(result_string)
    _, output_strain_list = knn01_nn.kneighbors(output_strain_dense.todense())

    list_strains = []
    for points in output_strain_list:
        for index in points:
            list_strains.append(index)
            
    return_list = [
        str(val)
        for val in list_strains
    ]

    records = parse_records(Cannabis.query.filter(Cannabis.strain_index.in_(return_list)).all())
    
    # MILESTONE 02 #> User input list goes through KNN model

    # return render_template("result_view.html")
    return jsonify(records)


@model_routes.route("/cannabis/output_nlp01", methods=['GET', 'POST'])
def nlp01_model_recommender():
    """creates list with top n recommended strains. <prod>

    Paramaters:
        request: dictionary (json object)
            user's strain description

        n: int, optional
            number of recommendations to return, default 3.

    Returns:
        list_model_id: python list of n recommended strains.
    """
    
    dict_list = request.form.get("dict_list")

    dict_list = (
        request.form.getlist("dict_list")
    )
    
    # MILESTONE 00 #> User request

    request_text = [dict_list.lower() for dict_list in dict_list]
    
    result_string = [' '.join(str(n) for n in request_text)] # Joins into a single string

    # MILESTONE 01 #> User request shown as list

    output_strain_dense = nlp01_tf.transform(result_string)
    _, output_strain_list = nlp01_nn.kneighbors(output_strain_dense.todense())

    list_strains = []
    for points in output_strain_list:
        for index in points:
            list_strains.append(index)
            
    return_list = [
        str(val)
        for val in list_strains
    ]

    records = parse_records(Cannabis.query.filter(Cannabis.strain_index.in_(return_list)).all())
    
    # MILESTONE 02 #> User input list goes through KNN model

    # return render_template("result_view.html", data=records)
    return jsonify(records)