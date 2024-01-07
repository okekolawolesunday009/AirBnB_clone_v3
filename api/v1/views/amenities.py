#!/usr/bin/python3
"""retrieves the ojects in states"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route('/amenities',  methods=['GET'], strict_slashes=False)
def show_amenity():
    """returns count of classes!"""
    amenities = storage.all(Amenity)
    amenities_list = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenities_list)


@app_views.route('amenities/<amenity_id>',  methods=['GET'], strict_slashes=False)
def Amenities_id(amenity_id):
    """returns count of classes!"""
    Amenities = storage.all(Amenity)
    for _, amenity_obj in Amenities.items():
         if amenity_obj.id == amenity_id:
             return jsonify(amenity_obj.to_dict())
    return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new State object."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a State object by ID."""
    amenties_to_delete = storage.get(Amenity, amenity_id)

    if not amenties_to_delete:
        abort(404)

    storage.delete(amenties_to_delete)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates a amenity
    """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)


