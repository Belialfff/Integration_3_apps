"""Belialfff"""
"""4 типа запросов(get,put,patch,delete) для таблицы customer"""


from flask import jsonify, request
from app import app, db, ma
from tables import Customer, Orders


"""Определение полей схемы"""
class CustomersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'customer_name', 'phone_number')

"""Условность Marshmallow для получения нескольких запросов, таким образом данные будут попадать в список"""
customers_schema_many = CustomersSchema(many=True)

@app.route('/customer/<id>', methods=['GET'])
def get_customers(id):
    """Роут для получения данных из таблицы customer по id, отсортированных по id, количество записей ограничено 15. Вид:
    [
        {
            "customer_name": "Татьяна",
            "id": 1,
            "phone_number": "89002001020"
        }
    ]"""
    get_customer = db.session.query(Customer).filter(Customer.id == id).order_by(Customer.id).limit(15)
    result = customers_schema_many.dump(get_customer)

    return jsonify(result)

@app.route('/customer', methods=['GET'])
def get_customers_all():

    """ Роут для получения всех записей из таблицы customer, отсортированных по id, количество записей ограничено 15. Вид:
    [
        {
            "customer_name": "Татьяна",
            "id": 1,
            "phone_number": "89002001020"
        }
    ]"""

    all_customers = Customer.query.order_by(Customer.id).limit(15)
    result = customers_schema_many.dump(all_customers)

    return jsonify(result)

@app.route('/customer/<id>', methods=['PATCH'])
def update_customers(id):
    """#Роут для обновления записи в таблице customer по id, возвращает обновлённый список записей с сортировкой по id, количество записей ограничено 15.
    Принимает данные вида:
    {

          "customer_name": str(not null),
          "phone_number" : str

    }"""
    id_req = id
    new_name = request.json['customer_name']
    new_number = request.json['phone_number']

    db.session.query(Customer).filter(Customer.id == id_req).update(dict(customer_name = new_name, phone_number = new_number))
    db.session.commit()

    customer_ = db.session.query(Customer).order_by(Customer.id).limit(15)
    result = customers_schema_many.dump(customer_)
    return jsonify(result)

@app.route('/customer/<id>', methods =['DELETE'])
def del_customers(id):

    """ Роут производит удаление заданного по id клиента из таблицы customer и связанные с ним по внешнему ключу записи из таблицы orders,
        возвращает обновлённый список записей с сортировкой по id, количество записей ограничено 15."""

    id_req = id
    db.session.query(Orders).filter(Orders.id_customer == id_req).delete()
    db.session.query(Customer).filter(Customer.id == id_req).delete()
    db.session.commit()

    customer_ = db.session.query(Customer).order_by(Customer.id).limit(15)
    result = customers_schema_many.dump(customer_)
    return jsonify(result)

@app.route('/customer', methods=['PUT'])
def new_customer():

    """ Роут выполняет добавление в таблицу customer новую запись, шаблон:
    {
      "customer_name": string(not null)
      "phone_number": string
    }
    возвращает обновлённый список записей с сортировкой по id, количество записей ограничено 15"""

    customer_name_req = request.json['customer_name']
    phone_number_req = request.json['phone_number']

    new_customer = Customer(customer_name_req, phone_number_req)

    db.session.add(new_customer)
    db.session.commit()

    customer_ = db.session.query(Customer).order_by(Customer.id).limit(15)
    result = customers_schema_many.dump(customer_)

    return jsonify(result)

