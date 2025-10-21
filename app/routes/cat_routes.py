from flask import abort, Blueprint, make_response
from app.models.cat import cats


cats_bp = Blueprint("cat_bp", __name__, url_prefix= "/cats")

@cats_bp.get("")
def get_all_cats():
    result_list = []
    for cat in cats:
        result_list.append(dict(
            id = cat.id,
            name=cat.name,
            color=cat.color,
            personality=cat.personality
        ))

    return result_list


#/cats/1  /cats/potato
@cats_bp.get("/<id>")
def get_single_cat(id):
    # id = int(id)

    cat = validate_cat(id) # 不需要存入一个东西里面
    
    cat_dict = dict(
            id = cat.id,
            name=cat.name,
            color=cat.color,
            personality=cat.personality
        )
    
    return cat_dict
    # for cat in cats:
    #     if cat.id == id:
    #         return dict(
    #         id = cat.id,
    #         name=cat.name,
    #         color=cat.color,
    #         personality=cat.personality
    #     )
            # wsm return cat不对？

    # return result
# 构建helper function，提高resuability。因为不止会get，还有patch，delet，都需要一个有效输入。
# 所以可以这样提取出来备用

def validate_cat(id):
    try:
        id = int(id)
    except ValueError: # 这里需要valueerror吗？因为这里是only可以得到的error，所以不太需要这个valueerror
        invalid = {"message": f"Cat id {id} is invalid."}

        # return invalid # 不想要这个，因为我们想要返回的是400的错误。
        abort(make_response(invalid, 400))

    for cat in cats:
        if cat.id == id:
            return cat
        
    not_found = {"message":  f"Cat with id ({id}) not fount"}
    abort(make_response(not_found, 404))


    
@cats_bp.get("/<name>")
def get_single_cat_by_name(name):

    for cat in cats:
        if cat.name == name:
            return dict(
            id = cat.id,
            name=cat.name,
            color=cat.color,
            personality=cat.personality
        )

