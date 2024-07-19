#!/usr/bin/env python3
"""
A basic flask app
"""
from flask import Flask, jsonify, Response, request, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    Fist route
    """
    return jsonify({
        'message': 'Bienvenue'
    })


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> Response:
    """
    Add users
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({
            "email": email,
            "message": "user created"
        })
    except ValueError:
        return jsonify({
            "message": "email already registered"
        }), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> Response:
    """
    Login Users
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        return abort(401)

    session_id = AUTH.create_session(email)

    response = jsonify({
        "email": email,
        "message": "logged in"
    })

    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> Response:
    """
    Log users out
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect("/")


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> Response:
    """
    Get the user
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
