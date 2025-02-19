import os
import binascii
from datetime import timedelta

from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_restful import Resource, Api, reqparse
from flask_migrate import Migrate
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

from src.database.base import db
from src.parse_data.parse_rozetka import get_products
from src. database import db_actions

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_URI")
app.config["JWT_SECRET_KEY"] = binascii.hexlify(os.urandom(24))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)
jwt_manager = JWTManager(app)



with app.app_context():
    # db.drop_all()
    db.create_all()
    # get_products()

class ProductAPI(Resource):
    def get(self, prod_id: str| None = None):
        if prod_id:
            product = db_actions.get_product(prod_id)
            responce = jsonify(product)
            responce.status_code = 200
            return responce
        
        products = db_actions.get_products()
        responce = jsonify(products)
        responce.status_code = 200
        return responce
    
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("description")
        parser.add_argument("img_url")
        parser.add_argument("price")
        kwargs = parser.parse_args()
        prod_id = db_actions.add_product(**kwargs)
        response = jsonify(f"Товар додано під id '{prod_id}' .")
        response.status_code = 201
        return response
    
    
    def put(self, prod_id: str):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("description")
        parser.add_argument("img_url")
        parser.add_argument("price")
        args = parser.parse_args()
        prod_id = db_actions.update_product(
            prod_id=prod_id,
            name=args.get("name"),
            description=args.get("description"),
            img_url=args.get("img_url"),
            price=args.get("price")
        )
        response = jsonify("Товар оновлено.")
        response.status_code = 200
        return response
    
    
    def delete(self, prod_id: str):
        db_actions.del_product(prod_id)
        response = jsonify("Товар видалено.")
        response.status_code = 204
        return response
    
    
    
class ReviewAPI(Resource):
    def get(self, rev_id: str| None = None):
        if rev_id:
            review = db_actions.get_review(rev_id)
            responce = jsonify(review)
            responce.status_code = 200
            return responce
        
        reviews = db_actions.get_reviews()
        responce = jsonify(reviews)
        responce.status_code = 200
        return responce
    
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        parser.add_argument("grade")
        kwargs = parser.parse_args()
        rev_id = db_actions.add_review(**kwargs)
        response = jsonify(f"Відгук додано під id '{rev_id}' .")
        response.status_code = 201
        return response
    
    
    def put(self, rev_id: str):
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        parser.add_argument("grade")
        args = parser.parse_args()
        rev_id = db_actions.update_review(
            rev_id=rev_id,
            text=args.get("text"),
            grade=args.get("grade")
        )
        response = jsonify("Відгук оновлено.")
        response.status_code = 200
        return response
    
    
    def delete(self, rev_id: str):
        db_actions.del_review(rev_id)
        response = jsonify("Відгук видалено.")
        response.status_code = 204
        return response



class UserAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = db_actions.get_user(user_id)
        resp = jsonify(user)
        user = resp.json
        del user["_password"]
        resp = jsonify(user)
        resp.status_code = 200
        return resp
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("first_name")
        parser.add_argument("last_name")
        parser.add_argument("email")
        parser.add_argument("password")
        kwargs = parser.parse_args()
        msg = db_actions.add_user(**kwargs)
        resp = jsonify(msg)
        resp.status_code = 201
        return resp
    
    
    
class TokenAPI(Resource):
    @jwt_required(refresh=True)
    def get(self):
        user_id = get_jwt_identity()
        token = dict(access_token = create_access_token(identity=user_id))
        resp = jsonify(token)
        resp._status_code =200
        return resp
    
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email")
        parser.add_argument("password")
        kwargs = parser.parse_args()
        tokens = db_actions.get_tokens(**kwargs)
        resp = jsonify(tokens)
        resp.status_code = 200
        return resp
        
    
api.add_resource(ProductAPI, "/api/products/", "/api/products/<prod_id>")
api.add_resource(ReviewAPI, "/api/reviews/", "/api/reviews/<rev_id>")
api.add_resource(UserAPI, "/api/users/")
api.add_resource(TokenAPI, "/api/tokens/")

if __name__ == "__main__":
    app.run(debug=True, port=3000)