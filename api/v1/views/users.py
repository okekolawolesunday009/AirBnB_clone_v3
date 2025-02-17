#!/usr/bin/python3
"""
retrieves the objects in users
"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route('/users',  methods=['GET'], strict_slashes=False)
def show_all_users():
    """returns count of classes user!"""
    users = storage.all(User)
    users_list = [user_obj.to_dict() for _, user_obj in users.items()]
    return jsonify(users_list)


@app_views.route('/users/<user_id>',  methods=['GET'], strict_slashes=False)
def get_users_id(user_id):
    """returns count of classes!"""
    user = storage.all(User)
    for _, user_obj in user.items():
        if user_obj.id == user_id:
            return jsonify(user_obj.to_dict())
    return abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_id(user_id):
    """Deletes a State object by ID."""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def updae_user_id(user_id):
    """
    Updates a User base on user_id
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users_create():
    """Creates a new user object."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'email' not in data:
        return jsonify({"error": "Missing email"}), 400
    elif 'password' not in data:
        return jsonify({"error": "Missing password"}), 400

    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201
