#!/usr/bin/python3
"""retrieves the ojects in states"""
from models import storage
from models.review import Review
from models.user import User
from models.place import Place
from api.v1.views import app_views
from werkzeug.exceptions import NotFound
from flask import jsonify, request, abort, make_response


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def show_all_reviews(place_id):
    """returns count of classes user!"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description=f"No Place found with place_id: {place_id}")

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('reviews/<review_id>',  methods=['GET'], strict_slashes=False)
def get_review_id(review_id):
    """returns a review object by id"""
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    return jsonify(review_obj.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review_id(review_id):
    """Deletes a review object by ID."""
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)

    storage.delete(review_obj)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review_id(review_id):
    """
    Updates a review base on review_id
    """
    review_obj = storage.get(Review, review_id)

    if not review_obj:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(review_obj, key, value)
    storage.save()
    return make_response(jsonify(review_obj.to_dict()), 200)


@app_views.route('places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def review_create(place_id):
    """Creates a new review object."""
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'text' not in data:
        return jsonify({"error": "Missing text"}), 400

    data['place_id'] = place_id

    new_Review = Review(**data)
    storage.new(new_Review)
    storage.save()
    return jsonify(new_Review.to_dict()), 201
