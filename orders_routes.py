"""Belialfff"""
"""4 типа запросов(get,put,patch,delete) для таблицы orders"""


from flask import jsonify, request
from app import app, db, ma
from tables import Orders


"""Определение полей схемы"""
class OrdersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'technic', 'price', 'id_customer')

"""Условность Marshmallow для получения нескольких запросов, таким образом данные будут попадать в список"""
orders_schema_many = OrdersSchema(many=True)

@app.route('/orders/<id>', methods=['GET'])
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

    get_order = db.session.query(Orders).filter(Orders.id == id).limit(15)
    result = orders_schema_many.dump(get_order)

    return jsonify(result)

@app.route('/orders', methods=['GET'])
def get_orders_all():

    """ Роут для полчения списка всех записей таблицы orders ,отсортированных по id, количество возвращаемых записей ограничено 15."""

    all_orders = db.session.query(Orders).order_by(Orders.id).limit(15)
    result = orders_schema_many.dump(all_orders)

    return jsonify(result)

@app.route('/orders/<id>', methods=['DELETE'])
def del_orders(id):

    """ Роут для удаления записи из таблицы orders по id, возвращает все записи таблицы orders, отсортированные по id,
    количество возвращаемых записей ограничено 15"""

    id_req = id
    db.session.query(Orders).filter(Orders.id == id_req).delete()
    db.session.commit()
    orders_ = db.session.query(Orders).order_by(Orders.id).limit(15)
    result = orders_schema_many.dump(orders_)

    return jsonify(result)

@app.route('/orders', methods=['PUT'])
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

    new_order = Orders( technic_req, price_req, id_customer_req)
    db.session.add(new_order)
    db.session.commit()
    orders_ = db.session.query(Orders).all()
    result = orders_schema_many.dump(orders_)

    return jsonify(result)

@app.route('/orders/<id>', methods=['PATCH'])
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

    db.session.query(Orders).filter(Orders.id == id_req).update(dict(technic = technic_req, price = price_req, id_customer = id_customer_req))
    db.session.commit()
    orders_ = db.session.query(Orders).order_by(Orders.id).limit(15)
    result = orders_schema_many.dump(orders_)

    return jsonify(result)