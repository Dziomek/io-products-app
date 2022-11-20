import flask
from . import app


@app.route('/', methods=['GET'])
def hello_world():
    response = flask.jsonify({"data": ["data1", "data2", "data3"]})

    return response
