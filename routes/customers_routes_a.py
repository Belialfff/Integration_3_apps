"""Belialfff"""
"""4 типа запросов(get,put,patch,delete) для таблицы customer"""


from flask import jsonify, request
from app_a import app_a, db_a, ma_a
from tables_a import Customer_a, Orders_a
import requests
import json

"""Определение полей схемы"""
class CustomersSchema(ma_a.Schema):
    class Meta:
        fields = ('id', 'customer_name', 'phone_number')

"""Условность Marshmallow для получения нескольких запросов, таким образом данные будут попадать в список"""
customers_schema_many = CustomersSchema(many=True)

@app_a.route('/customer/<id>', methods=['GET'])
def get_customers(id):
    """Роут для получения данных из таблицы customer по id, отсортированных по id, количество записей ограничено 15. Вид:
    [
        {
            "customer_name": "Татьяна",
            "id": 1,
            "phone_number": "89002001020"
        }
    ]"""
    get_customer = db_a.session.query(Customer_a).filter(Customer_a.id == id).order_by(Customer_a.id).limit(15)
    result = customers_schema_many.dump(get_customer)

    return jsonify(result)

@app_a.route('/customer', methods=['GET'])
def get_customers_all():

    """ Роут для получения всех записей из таблицы customer, отсортированных по id, количество записей ограничено 15. Вид:
    [
        {
            "customer_name": "Татьяна",
            "id": 1,
            "phone_number": "89002001020"
        }
    ]"""

    all_customers = Customer_a.query.order_by(Customer_a.id).limit(15)
    result = customers_schema_many.dump(all_customers)

    return jsonify(result)

@app_a.route('/customer/<id>', methods=['PATCH'])
def update_customers(id):
    """Роут выполняет изменение данных в таблице customer по id"""


    customer = Customer_a.query.get(id)

    if customer is None:
        return jsonify({"message": f"Запись c id {id} не найдена"}), 404

    customer_name_req = request.json.get('customer_name')
    phone_number_req = request.json.get('phone_number')

    if customer_name_req:
        customer.customer_name = customer_name_req
    if phone_number_req:
        customer.phone_number = phone_number_req

    try:
        db_a.session.commit()
        return jsonify({"message": f"Запись c id {id} успешно обновлена"}), 200
    except Exception as e:
        db_a.session.rollback()
        return jsonify({"message": f"Ошибка при обновлении записи: {str(e)}"}), 500

@app_a.route('/customer/<id>', methods =['DELETE'])
def del_customers(id):

    """ Роут производит удаление заданного по id клиента из таблицы customer и связанные с ним по внешнему ключу записи из таблицы orders,
        возвращает обновлённый список записей с сортировкой по id, количество записей ограничено 15."""

    id_req = id
    db_a.session.query(Orders_a).filter(Orders_a.id_customer == id_req).delete()
    db_a.session.query(Customer_a).filter(Customer_a.id == id_req).delete()
    db_a.session.commit()

    customer_ = db_a.session.query(Customer_a).order_by(Customer_a.id).limit(15)
    result = customers_schema_many.dump(customer_)
    return jsonify(result)

@app_a.route('/customer', methods=['PUT'])
def new_customer():

    """ Роут выполняет добавление в таблицу customer новую запись, шаблон:
    {
      "customer_name": string(not null)
      "phone_number": string
    }
    возвращает обновлённый список записей с сортировкой по id, количество записей ограничено 15"""

    customer_name_req = request.json['customer_name']
    phone_number_req = request.json['phone_number']

    new_customer = Customer_a(customer_name_req, phone_number_req)

    db_a.session.add(new_customer)
    db_a.session.commit()

    customer_data = {
        "customer_name": customer_name_req,
        "phone_number": phone_number_req,
        "price": 0
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:8002/clients', headers=headers, data=json.dumps(customer_data))

    if response.status_code == 200:

        customers_data = json.loads(response.content)
        return jsonify(customers_data)

    else:
        return jsonify({"message": "Ошибка при добавлении клиента во второе приложение"}), 500

    customer_ = db_a.session.query(Customer_a).order_by(Customer_a.id).limit(15)
    result = customers_schema_many.dump(customer_)
    print(result)
    return jsonify(result)

