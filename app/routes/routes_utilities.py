from flask import abort, make_response
from ..db import db

def validate_model(cls, id):
    try:
        id = int(id)
    except ValueError: # 这里需要valueerror吗？因为这里是only可以得到的error，所以不太需要这个valueerror
        invalid = {"message": f"{cls.__name__} id {id} is invalid."}
        # return invalid # 不想要这个，因为我们想要返回的是400的错误。
        abort(make_response(invalid, 400))

    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)

    # for cat in cats:
    #     if cat.id == id:
    #         return cat
    if not model:
        not_found = {"message":  f"{cls.__name__} with id ({id}) not fount"}
        abort(make_response(not_found, 404))

    return model