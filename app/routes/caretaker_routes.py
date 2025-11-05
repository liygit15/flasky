from ..routes.routes_utilities import validate_model, create_model, get_models_with_filters
from flask import abort, Blueprint, make_response, request
from ..models.caretaker import Caretaker
from ..models.cat import Cat
from ..db import db 


bp = Blueprint("caretakers_bp", __name__, url_prefix="/caretakers")

@bp.post("")
def create_caretaker():
    request_body = request.get_json()

    return create_model(Caretaker, request_body)

@bp.post("/<id>/cats")
def create_cat_with_caretaker_id(id):
    caretaker = validate_model(Caretaker, id)

    request_body = request.get_json()
    request_body["caretaker_id"] = caretaker.id

    return create_model(Cat, request_body)

@bp.get("")
def get_all_caretakers():
    return get_models_with_filters(Caretaker, request.args)

@bp.get("/<id>")
def get_caretaker(id):
    caretaker = validate_model(Caretaker, id)
    return caretaker.to_dict()

@bp.get("/<id>/cats")
def get_all_caretaker_cats(id):
    caretaker = validate_model(Caretaker, id)
    cats = [cat.to_dict() for cat in caretaker.cats]

    return cats