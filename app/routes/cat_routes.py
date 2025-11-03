from flask import  Blueprint, request,Response
from ..models.cat import Cat
from ..db import db
from .routes_utilities import validate_model

bp = Blueprint("cat_bp", __name__, url_prefix= "/cats")

@bp.post("")
def create_cat():
    request_body = request.get_json()
    # name = request_body["name"]
    # color = request_body["color"]
    # personality = request_body["personality"]

    # new_cat = Cat(
    #     name=name,
    #     color=color,
    #     personality=personality
    # )

    try:
        new_cat = Cat.from_dict(request_body)
    except KeyError as error:
        return {"error": f"Missing required field: {error.args[0]}"}, 400


    # new_cat = Cat.from_dict(request_body)
    db.session.add(new_cat)
    db.session.commit()

    return new_cat.to_dic(), 201


@bp.get("")
def get_all_cats():
    query = db.select(Cat)
    name_param =request.args.get("name")
    if name_param:
        # find exact match for name
        query = query.where(Cat.name == name_param)
        
    color_param = request.args.get("color")
    if color_param:
        query = query.where(Cat.color.ilike(f"%{color_param}%"))
    
    query = query.order_by(Cat.id)

    cats = db.session.scalars(query)
    result_list = []
    
    for cat in cats:
        result_list.append(cat.to_dict())

    return result_list


#find out if a name query parameter was provided
    # if name_param:
    #     #explain query arg by arg: 
    #     # query = db.select(Cat)  --> select all columns from Cat table
    #     #.where(Cat.name == name_param) --> filter the results where the name column matches the name_param value
    #     #.order_by(Cat.id) --> order the results by the id column
    #     query = db.select(Cat).where(Cat.name == name_param).order_by(Cat.id)

    # #if not, get all cats
    # if color_param:
    #     query = db.select(Cat).where(Cat.color.ilike(f"%{color_param}%")).order_by(Cat.id)
    # else:
    #     #build the query to get all cats ordered by their id
    #     query = db.select(Cat).order_by(Cat.id)





#/cats/1  /cats/potato
@bp.get("/<id>")
def get_single_cat(id):

    # query = db.select(Cat).where(Cat.id == id)
    # cat = db.session.scalar(query)
    cat = validate_model(Cat, id)
    
    return cat.to_dict()

    # for cat in cats:
    #     if cat.id == id:
    #         return dict(
    #         id = cat.id,
    #         name=cat.name,
    #         color=cat.color,
    #         personality=cat.personality
    #     )

    # return result


# # 构建helper function，提高resuability。因为不止会get，还有patch，delet，都需要一个有效输入。
# # 所以可以这样提取出来备用


    
# # @cats_bp.get("/<name>")
# # def get_single_cat_by_name(name):

# #     for cat in cats:
# #         if cat.name == name:
# #             return dict(
# #             id = cat.id,
# #             name=cat.name,
# #             color=cat.color,
# #             personality=cat.personality
# #         )



@bp.put("/<id>")
def replace_cat(id):
    cat = validate_model(Cat, id)

    request_body = request.get_json()
    cat.name = request_body["name"]
    cat.color = request_body["color"]
    cat.personality = request_body["personality"]

    db.session.commit()
    
    return Response(status=204, mimetype="application/json")


@bp.delete("/<id>")
def delete_cat(id):
    cat = validate_model(Cat, id)

    db.session.delete(cat)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
