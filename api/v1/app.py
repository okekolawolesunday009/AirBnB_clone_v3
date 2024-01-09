#!/usr/bin/python3
"""Contains a Flask web application API.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from flask_cors import CORS
import os


app = Flask(__name__)
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
CORS(app, resources={'/*': {'origins': [app_host]}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """ json 404 page """
    return make_response(jsonify({
        "error": "Not found"
        }), 404)


@app.teardown_appcontext
def teardown_storage(exception=None):
    """
    Teardown function to close the storage at the end of the app context.
    """
    storage.close()


if __name__ == '__main__':
    """where app is run"""
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True)
