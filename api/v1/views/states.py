#!/usr/bin/python3
"""retrieves the ojects in states"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify


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
    for state_id, state_obj in states.items():
        if state.id == state_id:
            return jsonify(state)

