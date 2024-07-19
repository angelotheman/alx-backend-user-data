#!/usr/bin/env python3
"""
A basic flask app
"""
from flask import Flask, jsonify, Response, request, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """
    Fist route
    """
    return jsonify({
        'message': 'Bienvenue'
    })


@app.route('/users', methods=['POST'])
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


@app.route('/sessions', methods=['POST'])
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


@app.route('/sessions', methods=['DELETE'])
def logout() -> Response:
    """
    Log users out
    """
    session_id = request.cookies.get('session_id')

    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        redirect("/")
    except NoResultFound:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
