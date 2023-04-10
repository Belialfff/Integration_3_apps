"""Belialfff"""
"""Файл с join sql запросами"""


from flask import jsonify, request
from app_a import app_a, db_a, ma_a
from tables_a import Customer_a, Orders_a
import json
import requests

"""Определение полей схемы"""
class CustomerOrdersSchema_a(ma_a.Schema):
    class Meta:
        fields = ('id', 'customer_name', 'phone_number', 'technic', 'price')

"""Условность Marshmallow для получения нескольких запросов, таким образом данные будут попадать в список"""
customers_orders_schema_many = CustomerOrdersSchema_a(many=True)

@app_a.route('/customer_orders', methods=['GET'])
def get_customer_orders():

    """Роут для получения полного списка клиентов и их заказов вида :
        [
            {
                "customer_name": "Татьяна",
                "id": 1,
                "phone_number": "89002001020",
                "price": 1600,
                "technic": "Смартфон"
            },
    Ограничение на 15 записей, сортировка по id клиента"""

    customers_orders = db_a.session.query(Customer_a.id, Customer_a.customer_name, Customer_a.phone_number, Orders_a.technic, Orders_a.price)\
        .select_from(Customer_a).join(Orders_a, Customer_a.id == Orders_a.id_customer).order_by(Customer_a.id).limit(15)
    result = customers_orders_schema_many.dump(customers_orders)

    return jsonify(result)

@app_a.route('/customer_orders/<string:name>', methods=['GET'])
def get_customer_orders_by_name(name):
    """Роут для получения списка техники и её стоимоти для заданного имени в таблице customer вида:
    {
        "customer_name: Татьяна [{'phone_number': '89002001020'}]": [
            {
                "price": 1600,
                "technic": "Смартфон"
            },
            {
                "price": 2500,
                "technic": "Ноутбук"
            }
        ]
    }"""
    customers_orders = db_a.session.query(Orders_a.technic, Orders_a.price)\
        .select_from(Customer_a).join(Orders_a, Customer_a.id == Orders_a.id_customer).\
        filter(Customer_a.customer_name == name).order_by(Customer_a.customer_name).all()
    result = customers_orders_schema_many.dump(customers_orders)
    phone_num = db_a.session.query(Customer_a.phone_number).filter(Customer_a.customer_name == name).limit(1)
    rusult_num = customers_orders_schema_many.dump(phone_num)

    return jsonify({f"customer_name: {name} {rusult_num}":result})

@app_a.route('/cis', methods=['GET'])
def get_customer_orders_by_phone():

    id_customer = request.json['id_customer']


    customers_orders = db_a.session.query(Customer_a.phone_number)\
        .select_from(Customer_a).join(Orders_a, Customer_a.id == Orders_a.id_customer).\
        filter(Customer_a.id == id_customer).all()
    result = customers_orders_schema_many.dump(customers_orders)

    return jsonify(result)

    customer_data = {

        "phone_number": result
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:8000/orders', headers=headers, data=json.dumps(customer_data))

    if response.status_code == 200:
        # получение обновленного списка клиентов из второго приложения

        customers_data = json.loads(response.content)
        return jsonify(customers_data)
    else:
        return jsonify({"message": "Ошибка"}), 500
