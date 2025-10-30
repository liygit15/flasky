import pytest
from app import create_app  # 为什么这样？
from app.db import db
from flask.signals import request_finished
from app.models.cat import Cat
from dotenv import load_dotenv
import os

load_dotenv()


# create test app 
@pytest.fixture # 第一个pytest.fixture 创建测试app
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI') # 连接到test database ，不会连接到别的错误数据库
    }

    app = create_app(test_config)  # 这里我们真的知道连接到了test database

    @request_finished.connect_via(app) # 这边和下面2个with都是常规的
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context(): # create 和 drop table
        db.create_all() # create table ，run migrattion 和update，得到我们想要的model 和table
        yield app

    with app.app_context(): # drop database
        db.drop_all()

@pytest.fixture # 第二个fixture，创建测试用户
def client(app):  # Client fixture which simulate a client making HTTP requests.
    return app.test_client()


@pytest.fixture # 第三个 创建sample data。因为post不需要数据库任何，get 需要数据库有数据
def one_cat(app):
    cat = Cat(
    name="MOrty",
    color="Orange", 
    personality="loves cords"
    )
    db.session.add(cat)
    db.session.commit()


