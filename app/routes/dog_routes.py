from flask import abort, Blueprint, make_response,request,Response
from ..models.dog import Dog
from ..db import db


dogs_bp = Blueprint("dog_bp", __name__, url_prefix= "/dogs")


@dogs_bp.post("")
def create_dog():
    request_body = request.get_json()
    name = request_body["name"]
    color = request_body["color"]
    breed = request_body["breed"]
    personality = request_body["personality"]

    new_dog = Dog(
        name=name,
        color=color,
        personality=personality,
        breed=breed
    )

    db.session.add(new_dog)
    db.session.commit()

    dog_response = dict(
        id=new_dog.id,
        name=new_dog.name,
        color=new_dog.color,
        breed=new_dog.breed,
        personality=new_dog.personality
    )
    
    return dog_response, 201


@dogs_bp.get("")
def get_all_dogs():
    query = db.select(Dog)
    name_param =request.args.get("name")
    if name_param:
        # find exact match for name
        query = query.where(Dog.name == name_param)
        
    color_param = request.args.get("color")
    if color_param:
        query = query.where(Dog.color.ilike(f"%{color_param}%"))
    
    query = query.order_by(Dog.id)

    dogs = db.session.scalars(query)
    result_list = []
    
    for dog in dogs:
        result_list.append(dict(
            id = dog.id,
            name=dog.name,
            color=dog.color,
            breed=dog.breed,
            personality=dog.personality
        ))

    return result_list
