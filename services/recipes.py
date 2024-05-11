import requests
from flask import Flask, jsonify, request, make_response
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*',
     allow_headers=['Content-Type', 'Authorization'])
app.config['SECRET_KEY'] = os.urandom(24)
port = int(os.environ.get('PORT', 5001))


@app.route("/")
def home():
    return "Hello, this is a Flask Microservice"


BASE_URL = "https://dummyjson.com"


@app.route('/recipes', methods=['GET'])
def get_recipes():
    response = requests.get(f"{BASE_URL}/recipes")
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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
