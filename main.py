import os

from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_restful import Resource, Api, reqparse
from src.database.models import db
from src.parse_data.parse_rozetka import get_products
from src. database import db_actions

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_URI")
db.init_app(app)
api = Api(app)



# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     get_products()

class ProductAPI(Resource):
    def row_to_data(self, products: list):
        data = []
        for product in products:
            data.append({
                "id":product.id,
                "name": product.name,
                "description": product.description,
                "img_url": product.img_url,
                "price": product.price
            })
        
        response = jsonify(data)
        response.status_code = 200
        return response
    
    
    def get(self, prod_id: str| None = None):
        if prod_id:
            product = db_actions.get_product(prod_id)
            return self.row_to_data([product])
        
        products = db_actions.get_products()
        return self.row_to_data(products)
    
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("description")
        parser.add_argument("img_url")
        parser.add_argument("price")
        args = parser.parse_args()
        prod_id = db_actions.add_product(
            name=args.get("name"),
            description=args.get("description"),
            img_url=args.get("img_url"),
            price=args.get("price")
        )
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
    def row_to_data(self, reviews: list):
        data = []
        for review in reviews:
            data.append({
                "id":review.id,
                "text": review.text,
                "grade": review.grade
            })
        
        response = jsonify(data)
        response.status_code = 200
        return response
    
    
    def get(self, rev_id: str| None = None):
        if rev_id:
            review = db_actions.get_review(rev_id)
            return self.row_to_data([review])
        
        reviews = db_actions.get_reviews()
        return self.row_to_data(reviews)
    
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        parser.add_argument("grade")
        args = parser.parse_args()
        rev_id = db_actions.add_review(
            text=args.get("text"),
            grade=args.get("grade")
        )
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
    
api.add_resource(ProductAPI, "/api/products/", "/api/products/<prod_id>", ReviewAPI, "/api/reviews/", "/api/reviews/<rev_id>")
# api.add_resource(ReviewAPI, "/api/reviews/", "/api/reviews/<rev_id>")

if __name__ == "__main__":
    app.run(debug=True, port=3000)