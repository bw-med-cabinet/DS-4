#> app/routes/model_app.py

#> import packages
from flask import Blueprint, jsonify, request, render_template
from app.models import Cannabis, db, parse_records

import pickle
import numpy
import json
import pandas as pd

from sklearn.neighbors import NearestNeighbors

model_routes = Blueprint("model_routes", __name__)


"""strain_type = [
    'Indica', 'Sativa', 'Hybrid'
]

effect_profile = [
    'Happy', 'Relaxed', 'Euphoric', 'Uplifted', 'Creative', 'Sleepy', 
    'Energetic', 'Focused', 'Hungry', 'Talkative', 'Tingly', 'Giggly', 
    'Aroused'
]

flavor_profile = [
    'Earthy', 'Sweet', 'Citrus', 'Pungent', 'Berry', 'Pine', 'Flowery', 
    'Woody', 'Spicy', 'Herbal', 'Lemon', 'Skunk', 'Tropical', 'Blueberry', 
    'Grape', 'Orange', 'Cheese', 'Pepper', 'Lime', 'Strawberry', 'Grapegruit', 
    'Sage', 'Mint', 'Pineapple', 'Lavender', 'Chemical', 'Vanilla', 'Mango', 
    'Honey', 'Tree', 'Fruit', 'Amonia', 'Menthol', 'Nutty', 'Coffee', 'Butter', 
    'Tea', 'Apple', 'Rose', 'Violet', 'Apricot', 'Tar', 'Chestnut', 'Tobacco', 
    'Peach', 'Pear', 'Plum'
]"""


dtm = pickle.load(open('./app/data/knn01_dtm.pkl', 'rb'))
tf = pickle.load(open('./app/data/knn01_tf.pkl', 'rb'))


@model_routes.route("/cannabis")
def cannabis():
    """database endpoint.

    Returns:
        dictionary (json object)
    """
    db_cannabis = Cannabis.query.all()
    cannabis_response = parse_records(db_cannabis)
    return jsonify(cannabis_response)


@model_routes.route("/cannabis/model_output", methods=['POST'])
def knn01_model_recommender():
    """creates list with top n recommended strains.

    Paramaters:
        request: dictionary (json object)
            list of user's strain description

        n: int, optional
            number of recommendations to return, default 5.

    Returns:
        list_model_id: python list of n recommended strains.
    """
    nn = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
    nn.fit(dtm)

    type_list = request.form.getlist("type_list")
    effect_list = request.form.getlist("effect_list")
    flavor_list = request.form.getlist("flavor_list")	
    
    # request_dict = {"effect": effect_dict, 
    #                "flavor": flavor_list
    #             } #> JSON dictionaries test

    request_text = [type_list,
                    effect_list, 
                    flavor_list                    
                ]
    
    result_text = [] # Merges input lists
    for sublist in request_text:
        for n in sublist:
            result_text.append(n)

    result_string = [' '.join(str(n) for n in result_text)] # Joins into a single string

    # MILESTONE 01 #> User input is shown as a list

    output_strain_dense = tf.transform(result_string)
    _, output_strain_list = nn.kneighbors(output_strain_dense.todense())

    list_strains = []
    for points in output_strain_list:
        for index in points:
            list_strains.append(index)
            
    return_list = [
        str(val)
        for val in list_strains
    ]

    records = parse_records(Cannabis.query.filter(Cannabis.model_id.in_(return_list)).all())
    
    # MILESTONE 02 #> User input list goes through KNN model

    return jsonify(records)
    