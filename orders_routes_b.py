"""Belialfff"""
"""4 типа запросов(get,put,patch,delete) для таблицы orders"""


from flask import jsonify, request
from app_a import db_a, app_a, ma_a
from tables_a import Orders_a, Customer_a
import json, requests

"""Определение полей схемы"""
class OrdersSchema(ma_a.Schema):
    class Meta:
        fields = ('id', 'technic', 'price', 'id_customer')

"""Условность Marshmallow для получения нескольких запросов, таким образом данные будут попадать в список"""
orders_schema_many = OrdersSchema(many=True)

class SnpSchema(ma_a.Schema):
    class Meta:
        fields = ('phone_number',)

"""Условность Marshmallow для получения нескольких запросов, таким образом данные будут попадать в список"""
customers_orders_schema_many = SnpSchema(many=True)

@app_a.route('/orders/<id>', methods=['GET'])
def get_orders(id):

    """Роут для полчения записи из таблицы orders по id вида:
    [
        {
            "id": 1,
            "id_customer": 1,
            "price": 1600,
            "technic": "Смартфон"
        }
    ] Сортировка по id , лимит записей 15"""

    get_order = db_a.session.query(Orders_a).filter(Orders_a.id == id).limit(15)
    result = orders_schema_many.dump(get_order)

    return jsonify(result)

@app_a.route('/orders', methods=['GET'])
def get_orders_all():

    """ Роут для полчения списка всех записей таблицы orders ,отсортированных по id, количество возвращаемых записей ограничено 15."""

    all_orders = db_a.session.query(Orders_a).order_by(Orders_a.id).limit(15)
    result = orders_schema_many.dump(all_orders)
    return jsonify(result)

@app_a.route('/orders/<id>', methods=['DELETE'])
def del_orders(id):

    """ Роут для удаления записи из таблицы orders по id, возвращает все записи таблицы orders, отсортированные по id,
    количество возвращаемых записей ограничено 15"""

    id_req = id
    db_a.session.query(Orders_a).filter(Orders_a.id == id_req).delete()
    db_a.session.commit()
    orders_ = db_a.session.query(Orders_a).order_by(Orders_a.id).limit(15)
    result = orders_schema_many.dump(orders_)

    return jsonify(result)

@app_a.route('/orders', methods=['PUT'])
def new_orders():

    """Роут выполняет добавление в таблицу orders новую запись, шаблон:
    {
      "id_customer" : int,
      "technic": string,
      "price": int
     }
    возвращает обновлённый список записей с сортировкой по id, количество записей ограничено 15"""

    technic_req = request.json['technic']
    price_req = request.json['price']
    id_customer_req = request.json['id_customer']

    new_order = Orders_a(technic_req, price_req, id_customer_req)
    db_a.session.add(new_order)
    db_a.session.commit()

    orders_ = db_a.session.query(Orders_a).all()
    result = orders_schema_many.dump(orders_)


    customers_orders = db_a.session.query(Customer_a.phone_number)\
        .select_from(Customer_a).join(Orders_a, Customer_a.id == Orders_a.id_customer).\
        filter(Customer_a.id == id_customer_req).all()
    nm = customers_orders_schema_many.dump(customers_orders)

    number = nm[0]

    a = number['phone_number']

    check_num = a

    customer_data = \
    {
       "price": price_req,
       "phone_number": str(check_num)
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:8002/clients_price', headers=headers,
                             data=json.dumps(customer_data))

    if response.status_code == 200:
        # получение обновленного списка клиентов из второго приложения

        customers_data = json.loads(response.content)
        return jsonify(customers_data)
    else:
        return jsonify({"message": "Ошибка"}), 500

    orders_ = db_a.session.query(Orders_a).all()
    result = orders_schema_many.dump(orders_)

    return jsonify(result)

@app_a.route('/orders/<id>', methods=['PATCH'])
def update_orders(id):

    """Роут для обновления записи в таблице orders по id, возвращает обновлённый список записей с сортировкой по id, количество записей ограничено 15.
    шаблон:
    {

            "id_customer": int,
            "technic" : str,
            "price" : int

    }"""

    id_req = id
    technic_req = request.json['technic']
    price_req = request.json['price']
    id_customer_req = request.json['id_customer']

    db_a.session.query(Orders_a).filter(Orders_a.id == id_req).update(dict(technic = technic_req, price = price_req, id_customer = id_customer_req))
    db_a.session.commit()
    orders_ = db_a.session.query(Orders_a).order_by(Orders_a.id).limit(15)
    result = orders_schema_many.dump(orders_)

    return jsonify(result)
