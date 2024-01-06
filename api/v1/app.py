#!/usr/bin/python3
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """ json 404 page """
    return make_response(jsonify({"error": "Not found"}), 404)

@app.teardown_appcontext 
def close():
    storage.close()


if __name__ == "__main__":
    # python -m api.v1.app
    if getenv('HBNB_API_HOST'):
        app.run(host=getenv('HBNB_API_HOST'), port=getenv('HBNB_API_PORT')
    else:
        app.run(host="0.0.0.0", port=5000)

