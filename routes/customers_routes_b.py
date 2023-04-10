"""Belialfff"""
"""4 типа запросов(get,put,patch,delete) для таблицы customer"""


from flask import jsonify, request
from app_b import app_b, db_b, ma_b
from tables_b import Customer_b, Orders_b


"""Определение полей схемы"""
class CustomersSchema(ma_b.Schema):
    class Meta:
        fields = ('id', 'customer_name', 'phone_number')

"""Условность Marshmallow для получения нескольких запросов, таким образом данные будут попадать в список"""
customers_schema_many = CustomersSchema(many=True)

@app_b.route('/customer/<id>', methods=['GET'])
def get_customers(id):
    """Роут для получения данных из таблицы customer по id, отсортированных по id, количество записей ограничено 15. Вид:
    [
        {
            "customer_name": "Татьяна",
            "id": 1,
            "phone_number": "89002001020"
        }
    ]"""
    get_customer = db_b.session.query(Customer_b).filter(Customer_b.id == id).order_by(Customer_b.id).limit(15)
    result = customers_schema_many.dump(get_customer)

    return jsonify(result)

@app_b.route('/customer', methods=['GET'])
def get_customers_all():

    """ Роут для получения всех записей из таблицы customer, отсортированных по id, количество записей ограничено 15. Вид:
    [
        {
            "customer_name": "Татьяна",
            "id": 1,
            "phone_number": "89002001020"
        }
    ]"""

    all_customers = Customer_b.query.order_by(Customer_b.id).limit(15)
    result = customers_schema_many.dump(all_customers)

    return jsonify(result)

@app_b.route('/customer/<id>', methods=['PATCH'])
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

    db_b.session.query(Customer_b).filter(Customer_b.id == id_req).update(dict(customer_name = new_name, phone_number = new_number))
    db_b.session.commit()

    customer_ = db_b.session.query(Customer_b).order_by(Customer_b.id).limit(15)
    result = customers_schema_many.dump(customer_)
    return jsonify(result)

@app_b.route('/customer/<id>', methods =['DELETE'])
def del_customers(id):

    """ Роут производит удаление заданного по id клиента из таблицы customer и связанные с ним по внешнему ключу записи из таблицы orders,
        возвращает обновлённый список записей с сортировкой по id, количество записей ограничено 15."""

    id_req = id
    db_b.session.query(Orders_b).filter(Orders_b.id_customer == id_req).delete()
    db_b.session.query(Customer_b).filter(Customer_b.id == id_req).delete()
    db_b.session.commit()

    customer_ = db_b.session.query(Customer_b).order_by(Customer_b.id).limit(15)
    result = customers_schema_many.dump(customer_)
    return jsonify(result)

@app_b.route('/customer', methods=['PUT'])
def new_customer():

    """ Роут выполняет добавление в таблицу customer новую запись, шаблон:
    {
      "customer_name": string(not null)
      "phone_number": string
    }
    возвращает обновлённый список записей с сортировкой по id, количество записей ограничено 15"""

    customer_name_req = request.json['customer_name']
    phone_number_req = request.json['phone_number']

    new_customer = Customer_b(customer_name_req, phone_number_req)

    db_b.session.add(new_customer)
    db_b.session.commit()

    customer_ = db_b.session.query(Customer_b).order_by(Customer_b.id).limit(15)
    result = customers_schema_many.dump(customer_)

    return jsonify(result)

