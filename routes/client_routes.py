"""Belialfff"""
"""Роуты для базы данных Clients"""


from flask import jsonify, request
from app_clients import app_clients, db_clients, ma_clients
from tables_clients import Clients
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

@app_clients.route('/clients_price', methods=['POST'])
def get_price():

    phone_req = request.json['phone_number']
    price_req = request.json['price']

    old_price = db_clients.session.query(Clients).filter(Clients.phone_number == phone_req).all()
    old_price_ = clients_schema_many.dump(old_price)
    print(old_price_)

    if len(old_price_) == 0:

        msg = {'message': 'error'}
        return jsonify(msg)
    else:
        raw_dict = old_price_[0]
        raw_price = raw_dict['price']
        price_sum = raw_price+price_req

        new_price = db_clients.session.query(Clients).filter(Clients.phone_number == phone_req)\
        .update({Clients.price: price_sum})
        db_clients.session.commit()

        result = {'message': 'Price updated successfully'}

        return jsonify(result)

@app_clients.route('/clients', methods=['GET'])
def get_all_clients():

    all_orders = db_clients.session.query(Clients).order_by(Clients.id).limit(30)
    result = clients_schema_many.dump(all_orders)

    return jsonify(result)

@app_clients.route('/clients/<id>', methods=['DELETE'])
def del_clients(id):

    """ Роут для удаления записи из таблицы clients по id, возвращает все записи таблицы orders, отсортированные по id,
    количество возвращаемых записей ограничено 15"""

    id_req = id

    db_clients.session.query(Clients).filter(Clients.id == id_req).delete()
    db_clients.session.commit()

    orders_ = db_clients.session.query(Clients).order_by(Clients.id).limit(15)

    result = clients_schema_many.dump(orders_)

    return jsonify(result)

@app_clients.route('/clients', methods=['PUT'])
def new_clients():

    """
     {
        "customer_name": "Евгений",
        "phone_number": "8943543534",
        "price": 913092
     }
    """
    name_req = request.json['customer_name']
    phone_number_req = request.json['phone_number']
    price_req = request.json['price']

    new_client = Clients(name_req, phone_number_req, price_req)
    db_clients.session.add(new_client)
    db_clients.session.commit()

    orders_ = db_clients.session.query(Clients).all()

    result = clients_schema_many.dump(orders_)

    return jsonify(result)

@app_clients.route('/clients/<int:id>', methods=['PATCH'])
def update_customer(id):

    """ Роут выполняет изменение данных в таблице customer по id"""


    customer = Clients.query.get(id)

    if customer is None:
        return jsonify({"message": f"Запись c id {id} не найдена"}), 404

    customer_name_req = request.json.get('customer_name')
    phone_number_req = request.json.get('phone_number')
    price_req = request.json.get('price')

    if customer_name_req:
        customer.customer_name = customer_name_req
    if phone_number_req:
        customer.phone_number = phone_number_req
    if price_req:
        customer.price = price_req

    try:
        db_clients.session.commit()
        return jsonify({"message": f"Запись c id {id} успешно обновлена"}), 200
    except Exception as e:
        db_clients.session.rollback()
        return jsonify({"message": f"Ошибка при обновлении записи: {str(e)}"}), 500
