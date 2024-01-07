#!/usrbin/python3
'''Contains the index view for the API.'''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/stats',  methods=['GET'], strict_slashes=False)
def show_stats():
    """returns count of classes!"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    new_objs = {}
    for i in range(len(classes)):
        new_objs[names[i]] = storage.count(classes[i])

    return jsonify(new_objs)


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    '''Gets the status of the API.
    '''
    return jsonify(status='OK')
