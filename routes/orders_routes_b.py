"""Belialfff"""
"""4 типа запросов(get,put,patch,delete) для таблицы orders"""


from flask import jsonify, request
from app_b import db_b, app_b, ma_b
from tables_b import Orders_b, Customer_b
import json, requests

"""Определение полей схемы"""
class OrdersSchema(ma_b.Schema):
    class Meta:
        fields = ('id', 'clin_type', 'price', 'id_customer')

"""Условность Marshmallow для получения нескольких запросов, таким образом данные будут попадать в список"""
orders_schema_many = OrdersSchema(many=True)

class SnpSchema(ma_b.Schema):
    class Meta:
        fields = ('phone_number',)

"""Условность Marshmallow для получения нескольких запросов, таким образом данные будут попадать в список"""
customers_orders_schema_many = SnpSchema(many=True)

@app_b.route('/orders/<id>', methods=['GET'])
def get_orders(id):

    """Роут для полчения записи из таблицы orders по id вида:
    [
        {
            "id": 1,
            "id_customer": 1,
            "price": 1600,
            "clin_type" : str,
        }
    ] Сортировка по id , лимит записей 15"""

    get_order = db_b.session.query(Orders_b).filter(Orders_b.id == id).limit(15)
    result = orders_schema_many.dump(get_order)

    return jsonify(result)

@app_b.route('/orders', methods=['GET'])
def get_orders_all():

    """ Роут для полчения списка всех записей таблицы orders ,отсортированных по id, количество возвращаемых записей ограничено 15."""

    all_orders = db_b.session.query(Orders_b).order_by(Orders_b.id).limit(15)
    result = orders_schema_many.dump(all_orders)
    return jsonify(result)

@app_b.route('/orders/<id>', methods=['DELETE'])
def del_orders(id):

    """ Роут для удаления записи из таблицы orders по id, возвращает все записи таблицы orders, отсортированные по id,
    количество возвращаемых записей ограничено 15"""

    id_req = id
    db_b.session.query(Orders_b).filter(Orders_b.id == id_req).delete()
    db_b.session.commit()
    orders_ = db_b.session.query(Orders_b).order_by(Orders_b.id).limit(15)
    result = orders_schema_many.dump(orders_)

    return jsonify(result)

@app_b.route('/orders', methods=['PUT'])
def new_orders():

    """Роут выполняет добавление в таблицу orders новую запись, шаблон:
    {
      "id_customer" : int,
      "clin_type" : str,
      "price": int
     }
    возвращает обновлённый список записей с сортировкой по id, количество записей ограничено 15"""

    clin_type_req = request.json['clin_type']
    price_req = request.json['price']
    id_customer_req = request.json['id_customer']

    new_order = Orders_b(clin_type_req, price_req, id_customer_req)
    db_b.session.add(new_order)
    db_b.session.commit()

    orders_ = db_b.session.query(Orders_b).all()
    result = orders_schema_many.dump(orders_)


    customers_orders = db_b.session.query(Customer_b.phone_number)\
        .select_from(Customer_b).join(Orders_b, Customer_b.id == Orders_b.id_customer).\
        filter(Customer_b.id == id_customer_req).all()
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

        customers_data = json.loads(response.content)
        return jsonify(customers_data)
    else:
        return jsonify({"message": "Ошибка"}), 500

    orders_ = db_b.session.query(Orders_b).all()
    result = orders_schema_many.dump(orders_)

    return jsonify(result)

@app_b.route('/orders/<id>', methods=['PATCH'])
def update_orders(id):

    """Роут для обновления записи в таблице orders по id, возвращает обновлённый список записей с сортировкой по id, количество записей ограничено 15."""


    order = Orders_b.query.get(id)

    if order is None:
        return jsonify({"message": f"Запись c id {id} не найдена"}), 404

    customer_id_req = request.json.get('id_customer')
    clin_type_req = request.json.get('clin_type')
    price_req = request.json.get('price')

    if customer_id_req:
        order.id_customer = customer_id_req
    if clin_type_req:
        order.clin_type = clin_type_req
    if price_req:
        order.price = price_req

    try:
        db_b.session.commit()
        return jsonify({"message": f"Запись c id {id} успешно обновлена"}), 200
    except Exception as e:
        db_b.session.rollback()
        return jsonify({"message": f"Ошибка при обновлении записи: {str(e)}"}), 500
