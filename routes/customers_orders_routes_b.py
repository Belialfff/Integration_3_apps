"""Belialfff"""
"""Файл с join sql запросами"""


from flask import jsonify
from app_a import app_a, db_a, ma_a
from tables_a import Customer_a, Orders_a
import requests
import json

"""Определение полей схемы"""
class CustomerOrdersSchema_a(ma_a.Schema):
    class Meta:
        fields = ('id', 'customer_name', 'phone_number', 'technic', 'price')

"""Условность Marshmallow для получения нескольких запросов, таким образом данные будут попадать в список"""
customers_orders_schema_many = CustomerOrdersSchema_a(many=True)

@app_a.route('/customer_orders_b', methods=['GET'])
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

@app_a.route('/customer_orders_b/<string:ph_n>', methods=['GET'])
def get_customer_orders_by_name(ph_n):
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
    customers_orders = db_a.session.query(Orders_a.technic, Orders_a.price)\
        .select_from(Customer_a).join(Orders_a, Customer_a.id == Orders_a.id_customer).\
        filter(Customer_a.customer_name == ph_n).order_by(Customer_a.customer_name).all()
    result = customers_orders_schema_many.dump(customers_orders)
    phone_num = db_a.session.query(Customer_a.phone_number).filter(Customer_a.customer_name == ph_n).limit(1)
    rusult_num = customers_orders_schema_many.dump(phone_num)

    return jsonify({f"customer_name: {ph_n} {rusult_num}": result})
