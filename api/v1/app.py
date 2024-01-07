#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)

@app.errorhandler(404)
def not_found(error):
    """ json 404 page """
    return jsonify({"error": "Not found"})

@app.teardown_appcontext
def teardown_storage(exception):
    """
    Teardown function to close the storage at the end of the app context.
    """
    storage.close()


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST')
    port = int(os.environ.get('HBNB_API_PORT'))

    app.run(host=host, port=port, threaded=True, debug=True)
