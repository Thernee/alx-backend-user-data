#!/usr/bin/env python3

"""
Basic Flask app module
"""
from flask import Flask, jsonify, request, abort
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def basic() -> str:
    """
    Basic flask app
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
    Implement POST /users route
    """
    password = request.form.get('password')
    email = request.form.get('email')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """User login"""
    password = request.form.get('password')
    email = request.form.get('email')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        return_message = jsonify({"email": email, "message": "logged in"})
        return_message.set_cookie("session_id", session_id)
        return return_message
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
