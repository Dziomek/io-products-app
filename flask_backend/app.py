import flask
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def hello_world():
    response = flask.jsonify({"data": ["data1", "data2", "data3"]})

    return response


if __name__ == '__main__':
    app.run()