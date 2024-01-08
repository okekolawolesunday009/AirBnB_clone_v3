#!/usr/bin/python3
"""retrieves the ojects in states"""
from models import storage
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def city_Place(city_id):
    """returns count of classes user!"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',  methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    """"returns a place object by id"""
    review_obj = storage.get(Place, place_id)
    if not review_obj:
        abort(404)
    return jsonify(review_obj.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place_id(place_id):
    """Deletes a Place object by ID."""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def place_create(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        return jsonify({"error": "Missing text"}), 400

    data['city_id'] = city_id

    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_user_id(place_id):
    """
    Updates a Place base on user_id
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(Place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
