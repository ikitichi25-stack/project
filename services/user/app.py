from datetime import datetime, timedelta
import os
from flask import Flask, jsonify, request
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
JWT_SECRET = os.getenv('JWT_SECRET', 'change-me')
users = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400
    if username in users:
        return jsonify({'error': 'user exists'}), 409
    users[username] = {
        'password': generate_password_hash(password),
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    return jsonify({'message': 'user registered'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    user = users.get(username)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'invalid credentials'}), 401
    token = jwt.encode(
        {'sub': username, 'exp': datetime.utcnow() + timedelta(hours=1)},
        JWT_SECRET,
        algorithm='HS256'
    )
    return jsonify({'access_token': token})

@app.route('/profile', methods=['GET'])
def profile():
    auth = request.headers.get('Authorization', '')
    token = auth.replace('Bearer ', '')
    if not token:
        return jsonify({'error': 'authorization required'}), 401
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'invalid token'}), 401
    return jsonify({'username': payload['sub'], 'issued_at': payload['iat']}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
