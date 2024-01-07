#!/usr/bin/python3
"""retrieves the ojects in states"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states',  methods=['GET'], strict_slashes=False)
def show_states():
    """returns count of classes!"""
    states = storage.all(State)
    state_list = [state_obj.to_dict() for state_id, state_obj in states.items()]
    return jsonify(state_list)


@app_views.route('/states/<state_id>',  methods=['GET'], strict_slashes=False)
def states_id(state_id):
    """returns count of classes!"""
    states = storage.all(State)
    for _, state_obj in states.items():
         if state_obj.id == state_id:
             return jsonify(state_obj.to_dict())
    return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**data)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by ID."""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)



@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)


