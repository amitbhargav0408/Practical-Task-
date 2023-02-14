from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, JWTManager, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from datetime import timedelta
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '#$%@#$' 
jwt = JWTManager(app)

# connect to MongoDB
client=MongoClient("mongodb+srv://movieapi:123@movieapi.qe8d9xf.mongodb.net/?retryWrites=true&w=majority")
db = client["movieapi"]
users_collection = db['Users']
products_collection = db['products']

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    name = request.json.get('name')
    if not email or not password or not name:
        return jsonify({'message': 'All fields are required'}), 400
    if users_collection.find_one({'email': email}):
        return jsonify({'message': 'Email already registered'}), 400
    hashed_password = generate_password_hash(password)
    user = {'email': email, 'password': hashed_password, 'name': name}
    users_collection.insert_one(user)
    return jsonify({'message': 'User created successfully'})

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400
    user = users_collection.find_one({'email': email})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid email or password'}), 401
    access_token = create_access_token(identity=user['email'], expires_delta=timedelta(hours=5))
    return jsonify({'access_token': access_token})

@app.route('/productdetails',methods=['GET'])
@jwt_required()
def get_products():
    search = request.args.get('search')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    query = {}
    if search:
        query['$or'] = [
            {'title': {'$regex': search, '$options': 'i'}},
            {'description': {'$regex': search, '$options': 'i'}}
        ]
    if min_price:
        query['price'] = {'$gte': float(min_price)}
    if max_price:
        if 'price' in query:
            query['price']['$lte'] = float(max_price)
        else:
            query['price'] = {'$lte': float(max_price)}
    products = products_collection.find(query)
    return jsonify({'products': [product for product in products]})

@app.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    title = request.form.get('title')
    description = request.form.get('description')
    images = request.form.get('images')
    price = request.form.get('price')
    discount = request.form.get('discount', 0.0)
    if not title or not description or not images or not price:
        return jsonify({'message': 'Title, description, images, and price are required'}), 400

    product = { 'title': title, 'description':description, 'images': images, 'price':price,'discount':discount }
        
    products_collection.insert_one(product)
    return jsonify({'message': 'User created successfully'})
    




if __name__ == '__main__':
    app.run()