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


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token_route() -> Response:
    """
    Reset your password
    """
    email = request.form.get('email')

    if not email:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({
        "email": email,
        "reset_token": reset_token
    }), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> Response:
    """
    Update password finally
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    is_password_changed = False

    try:
        AUTH.update_password(reset_token, new_password)
        is_password_changed = True
    except ValueError:
        is_password_changed = False

    if not is_password_changed:
        abort(403)

    return jsonify({
        "email": email,
        "message": "Password updated"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
