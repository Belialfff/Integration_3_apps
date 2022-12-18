from app import app
from flask import jsonify

@app.route('/', methods = ['GET'])
def get_():
    return jsonify({'msg': 'Hello World'})