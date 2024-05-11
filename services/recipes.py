import requests
from flask import Flask, jsonify, request, make_response
import jwt
from functools import wraps
import json
import os
from jwt.exceptions import DecodeError

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
port = int(os.environ.get('PORT', 5001))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({'error': 'Authorization token is missing'}), 401
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
        except DecodeError:
            return jsonify({'error': 'Authorization token is invalid'}), 401
        return f(current_user_id, *args, **kwargs)
    return decorated


@app.route("/")
def home():

    return "Hello, this is a Flask Microservice"


BASE_URL = "https://dummyjson.com"


@app.route('/recipes', methods=['GET'])
@token_required
def get_recipes(current_user_id):
    headers = {'Authorization': f'Bearer {request.cookies.get("token")}'}
    response = requests.get(f"{BASE_URL}/recipes", headers=headers)
    if response.status_code != 200:
        return jsonify({'error': response.json()['message']}), response.status_code
    recipes = []
    for recipe in response.json()['recipes']:
        recipe_data = {
            'id': recipe['id'],
            'name': recipe['name'],
            'ingredients': recipe['ingredients'],
            'instructions': recipe['instructions'],
            'prepTimeMinutes': recipe['prepTimeMinutes'],
            'cookTimeMinutes': recipe['cookTimeMinutes'],
            'servings': recipe['servings'],
            'difficulty': recipe['difficulty'],
            'cuisine': recipe['cuisine']
        }
        recipes.append(recipe_data)
    return jsonify({'data': recipes}), 200 if recipes else 204


with open('users.json', 'r') as f:
    users = json.load(f)


@app.route('/auth', methods=['POST'])
def authenticate_user():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415
    username = request.json.get('username')
    password = request.json.get('password')
    for user in users:
        if user['username'] == username and user['password'] == password:
            token = jwt.encode(
                {'user_id': user['id']}, app.config['SECRET_KEY'], algorithm="HS256")
            response = make_response(
                jsonify({'message': 'Authentication successful'}))
            response.set_cookie('token', token)
            return response, 200
    return jsonify({'error': 'Invalid username or password'}), 401


if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=port)