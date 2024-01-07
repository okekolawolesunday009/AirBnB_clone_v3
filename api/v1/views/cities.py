#!/usr/bin/python3
"""retrieves the ojects in states"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route('/states/<state_id>/cities',  methods=['GET'], strict_slashes=False)
def show_states_city(state_id):
    """returns count of classes!"""
    states = storage.all(State)
    for _, state_obj in states.items():
        if state_obj.id == state_id:
            cities = [city.to_dict() for city in state_obj.cities]
            return jsonify(cities)
    return abort(404)


@app_views.route('/cities/<city_id>',  methods=['GET'], strict_slashes=False)
def cities_id(city_id):
    """returns count of classes!"""
    cities = storage.all(City)
    for _, city_obj in cities.items():
         if city_obj.id == city_id:
             return jsonify(city_obj.to_dict())
    return abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a new State object."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    states = storage.get(State, state_id)
    if not states:
        abort(404)

    new_city = City(**data)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a State object by ID."""
    city = storage.get(City, city_id)
    print(city)

    if not city:
         abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)



@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates a State
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'state_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
