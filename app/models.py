# app/models.py

#> import packages
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

migrate = Migrate()


class Cannabis(db.Model):
    """Cannabis database class"""
    strain_index = db.Column(db.String)
    model_id = db.Column(db.String, primary_key=True)
    strain_name = db.Column(db.String)
    strain_type = db.Column(db.String)
    strain_rating = db.Column(db.String)
    effect_profile = db.Column(db.String)
    flavor_profile = db.Column(db.String)
    strain_description = db.Column(db.String)


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