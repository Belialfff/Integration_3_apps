"""Belialfff"""
"""Файл с join sql запросами"""


from flask import jsonify, request
from app_clients import app_clients, db_clients, ma_clients
from tables_clients import Clients
import requests
import json

"""Определение полей схемы"""
class ClientsSchema(ma_clients.Schema):
    class Meta:
        fields = ('id', 'customer_name', 'phone_number', 'price')

"""Условность Marshmallow для получения нескольких запросов, таким образом данные будут попадать в список"""
clients_schema_many = ClientsSchema(many=True)

@app_clients.route('/clients', methods=['POST'])
def get_clients():

    customer_name_req = request.json['customer_name']
    phone_number_req = request.json['phone_number']
    price_req = request.json['price']

    new_client = Clients(customer_name_req, phone_number_req, price_req)

    db_clients.session.add(new_client)
    db_clients.session.commit()

    customer_ = db_clients.session.query(Clients).order_by(Clients.id).limit(15)
    result = clients_schema_many.dump(customer_)

    return jsonify(result)

@app_clients.route('/clients_price', methods=['GET'])
def get_price():

    phone = request.json['phone_number']

    customer_ = db_clients.session.query(Clients).filter(Clients.phone_number == phone).limit(15)
    result = clients_schema_many.dump(customer_)

    return jsonify(result)