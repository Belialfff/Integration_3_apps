"""Belialfff"""
"""Файл с join sql запросами"""


from flask import jsonify
from app import app, db, ma
from tables import Customer, Orders


"""Определение полей схемы"""
class CustomerOrdersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'customer_name', 'phone_number', 'technic', 'price')

"""Условность Marshmallow для получения нескольких запросов, таким образом данные будут попадать в список"""
customers_orders_schema_many = CustomerOrdersSchema(many=True)

@app.route('/customer_orders', methods=['GET'])
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

    customers_orders = db.session.query(Customer.id, Customer.customer_name, Customer.phone_number, Orders.technic, Orders.price)\
        .select_from(Customer).join(Orders, Customer.id == Orders.id_customer).order_by(Customer.id).limit(15)
    result = customers_orders_schema_many.dump(customers_orders)

    return jsonify(result)

@app.route('/customer_orders/<string:name>', methods=['GET'])
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
    customers_orders = db.session.query(Orders.technic, Orders.price)\
        .select_from(Customer).join(Orders, Customer.id == Orders.id_customer).filter(Customer.customer_name == name).order_by(Customer.customer_name).all()
    result = customers_orders_schema_many.dump(customers_orders)

    phone_num = db.session.query(Customer.phone_number).filter(Customer.customer_name == name).limit(1)
    rusult_num = customers_orders_schema_many.dump(phone_num)

    return jsonify({f"customer_name: {name} {rusult_num}":result})
