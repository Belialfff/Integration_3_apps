"""Belialfff"""
"""Файл с join sql запросами"""


from flask import jsonify, request
from app_b import app_b, db_b, ma_b
from tables_b import Customer_b, Orders_b
import requests
import json

"""Определение полей схемы"""
class CustomerOrdersSchema_b(ma_b.Schema):
    class Meta:
        fields = ('id', 'customer_name', 'phone_number', 'clin_type', 'price')

"""Условность Marshmallow для получения нескольких запросов, таким образом данные будут попадать в список"""
customers_orders_schema_many = CustomerOrdersSchema_b(many=True)

@app_b.route('/customer_orders_b', methods=['GET'])
def get_customer_orders():

    """Роут для получения полного списка клиентов и их заказов вида :
        [
            {
                "customer_name": "Татьяна",
                "id": 1,
                "phone_number": "89002001020",
                "price": 1600,
                "clin_type": "Лёгкая уборка"
            },
    Ограничение на 15 записей, сортировка по id клиента"""

    customers_orders = db_b.session.query(Customer_b.id, Customer_b.customer_name, Customer_b.phone_number, Orders_b.clin_type, Orders_b.price)\
        .select_from(Customer_b).join(Orders_b, Customer_b.id == Orders_b.id_customer).order_by(Customer_b.id).limit(15)

    result = customers_orders_schema_many.dump(customers_orders)

    return jsonify(result)

@app_b.route('/customer_orders_b/<string:name>', methods=['GET'])
def get_customer_orders_by_name(name):
    """Роут для получения списка техники и её стоимоти для заданного имени в таблице customer вида:
    {
        "customer_name: Татьяна [{'phone_number': '89002001020'}]": [
            {
                "price": 1600,
                "clin_type": "Уборка после вечеринки"
            },
            {
                "price": 2500,
                "clin_type": "Новоселье"
            }
        ]
    }"""
    customers_orders = db_b.session.query(Orders_b.clin_type, Orders_b.price)\
        .select_from(Customer_b).join(Orders_b, Customer_b.id == Orders_b.id_customer).\
        filter(Customer_b.customer_name == name).order_by(Customer_b.customer_name).all()

    result = customers_orders_schema_many.dump(customers_orders)

    phone_num = db_b.session.query(Customer_b.phone_number).filter(Customer_b.customer_name == name).limit(1)

    rusult_num = customers_orders_schema_many.dump(phone_num)

    return jsonify({f"customer_name: {name} {rusult_num}": result})

@app_b.route('/<id_customer>', methods=['GET'])
def get_customer_orders_by_phone(id_customer):

    id_customer = request.json['id_customer']


    customers_orders = db_b.session.query(Customer_b.phone_number)\
        .select_from(Customer_b).join(Orders_b, Customer_b.id == Orders_b.id_customer).\
        filter(Customer_b.id == id_customer).all()

    result = customers_orders_schema_many.dump(customers_orders)

    return jsonify(result)

    customer_data = {

        "phone_number": result

    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:8000/orders', headers=headers, data=json.dumps(customer_data))

    if response.status_code == 200:

        customers_data = json.loads(response.content)

        return jsonify(customers_data)
    else:
        return jsonify({"message": "Ошибка"}), 500
