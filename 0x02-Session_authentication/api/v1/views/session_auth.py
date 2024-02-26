#!/usr/bin/env python3

"""
Module of SessionAuth
"""
from flask import jsonify, request, Flask
from api.v1.views import app_views
from api.v1.views.users import User
from os import getenv

app = Flask(__name__)


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    POST /api/v1/auth_session/login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    elif password is None or email == '':
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if not user[0]:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    session_name = getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
