#!/usr/bin/python3
"""Python flash script to create crud operations for User class"""


from flask import jsonify, make_response, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """getting all the users from the database"""
    users = storage.all(User).values()
    users_dict = [user.to_dict() for user in users]
    return jsonify(users_dict)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Getting user by the Id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delte_user(user_id):
    """Deleting user from the database"""
    user = storage(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ creating a new user"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    user_oject = request.get_json()
    new_user = User(**user_oject)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict())
