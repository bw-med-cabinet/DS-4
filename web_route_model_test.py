#> app/routes/model_app.py > Local file structure

#> import statements
# from flask import Blueprint, jsonify, request, render_template
# from app.models import Cannabis, db, parse_records
#> From those you need jsonify, and requests

import pickle
import json

# DS-package dependencies
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy

#> Local flask blueprint, you might not need this?
model_routes = Blueprint("model_routes", __name__)

#> Pickle objects
dtm = pickle.load(open('./app/data/knn01_dtm.pkl', 'rb'))
tf = pickle.load(open('./app/data/knn01_tf.pkl', 'rb'))
# Change .pkl file directory as needed

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#> Function boiler-plate to parse data
def parse_records(database_records):
    """
    A helper method for converting a list of database record objects into a list of dictionaries, so they can be returned as JSON

    Param: database_records (a list of db.Model instances)

    Example: parse_records(User.query.all())

    """
    parsed_records = []
    for record in database_records:
        print(record)
        parsed_record = record.__dict__
        del parsed_record["_sa_instance_state"]
        parsed_records.append(parsed_record)
    return parsed_records

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#> Model endpoint
# Recieves user input as a list to output a JSON dictionary of n recommendations (default: 5)
@model_routes.route("/cannabis/model_output", methods=['GET', 'POST'])
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

    type_list = request.form.getlist("type_list")     # I'm not sure what data
    effect_list = request.form.getlist("effect_list") # type is the request.
    flavor_list = request.form.getlist("flavor_list") # outputting as?
    
    # MILESTONE 01 #> User input is stored
    # The code above this works as stated
    
    # request_dict = {"effect": effect_dict, 
    #                "flavor": flavor_list
    #             } > Testing to recieve input as JSON dictionary

    # This throws user input as a list of lists
    request_text = [type_list,
                    effect_list, 
                    flavor_list                    
                ]
    
    result_text = [] # Merges input lists
    for sublist in request_text:
        for n in sublist:
            result_text.append(n)

    # Joins into a single string
    result_string = [' '.join(str(n) for n in result_text)]

    # MILESTONE 02 #> User input is shown as a list
    # The code above this works as stated

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
    
    # MILESTONE 03 #> User input list goes through KNN model
    # The code above this works as stated

    # Remove milestones for testing
    
    return jsonify(records)