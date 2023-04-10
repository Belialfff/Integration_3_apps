from app_a import app_a
from flask import jsonify

@app_a.route('/', methods = ['GET'])
def get_():
    return jsonify({'msg': 'Hello World'})