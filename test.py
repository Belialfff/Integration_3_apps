from app_a import app_a
from app_b import app_b
from app_clients import app_clients
from flask import jsonify


@app_a.route('/', methods=['GET'])
def get_():
    return jsonify({'msg': 'Hello World'})


@app_b.route('/', methods=['GET'])
def get_():
    return jsonify({'msg': 'Hello World'})


@app_clients.route('/', methods=['GET'])
def get_():
    return jsonify({'msg': 'Hello World'})
