# app/routes/development.py

#> import packages
from flask import Blueprint, jsonify, request, render_template
from app.models import Cannabis, db, parse_records

import json


dev_routes = Blueprint("dev_routes", __name__)


@dev_routes.route("/cannabis/dev/model_form")
def user_form(): # <dev>
    """recommender user form.

    Returns:
        request: dictionary (json object)
            list of user's strain description
            
        schema:
        {"type_list": [""],
        "effect_list": [""],
        "flavor_list": [""]}
    """
    return render_template("user_form.html")


@dev_routes.route("/cannabis/dev/form_result", methods=['GET', 'POST'])
def model_form_recommender(): # <dev>
    """creates list with top n recommended strains.

    Paramaters:
        request: dictionary (json object)
            list of user's strain description

        n: int, optional
            number of recommendations to return, default 5.

    Returns:
        list_model_id: python list of n recommended strains.
    """
    type_list = request.form.get("type_list")
    effect_list = request.form.get("effect_list")
    flavor_list = request.form.get("flavor_list")	

    # MILESTONE 00 #> User request

    type_list, effect_list, flavor_list = (
        request.form.getlist("type_list"),
        request.form.getlist("effect_list"),
        request.form.getlist("flavor_list")
    )

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

    result_string = [' '.join(str(n) for n in result_text)]
    result_string = result_string.lower() # Normalize input

    # MILESTONE 01 #> User request shown as list

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

    # MILESTONE 02 #> knn_01 model result
    
    records = parse_records(Cannabis.query.filter(Cannabis.strain_index.in_(return_list)).all())

    return jsonify(records)