from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

users = {}
next_id = 1

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.route('/')
def home():
    return jsonify({"status": "ok"})

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values()))

@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Validation
    if not name or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    if email in [user['email'] for user in users.values()]:
        return jsonify({'error': 'Email already exists'}), 400

    hashed_password = generate_password_hash(password)

    user = {
        'id': next_id,
        'name': name,
        'email': email,
        'password': hashed_password
    }
    users[next_id] = user
    next_id += 1

    return jsonify(user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    user = users[user_id]

    user['name'] = data.get('name', user['name'])

    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404

    del users[user_id]
    return jsonify({'message': 'User deleted'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    for user in users.values():
        if user['email'] == email and check_password_hash(user['password'], password):
            return jsonify({'message': 'Login successful'})

    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
