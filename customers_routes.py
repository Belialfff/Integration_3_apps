
from app import app, jsonify, db, request, ma
from tables import Customer, Orders

class Customers_schema(ma.Schema):
    class Meta:
        fields = ('id', 'customer_name', 'phone_number')
customers_schema_many = Customers_schema(many = True)

# Роут для получения данных из таблицы customer по id, отсортированных по id, количество записей ограничено 15. Вид:
# [
#     {
#         "customer_name": "Татьяна",
#         "id": 1,
#         "phone_number": "89002001020"
#     }
# ]
@app.route('/customer/<id>', methods = ['GET'])
def get_customers(id):
    get_customer = db.session.query(Customer).filter(Customer.id == id).order_by(Customer.id).limit(15)
    result = customers_schema_many.dump(get_customer)
    return jsonify(result)


#Роут для получения всех записей из таблицы customer, отсортированных по id, количество записей ограничено 15
@app.route('/customer', methods=['GET'])
def get_customers_all():
    all_customers = Customer.query.order_by(Customer.id).limit(15)
    result = customers_schema_many.dump(all_customers)
    return jsonify(result)

#Роут для обновления записи в таблице customer по id, возвращает обновлённый список записей с сортировкой по id, количество записей ограничено 15.
# #{
#
#         "customer_name": str,
#         "phone_number" : str
#
# #}
@app.route('/customer/<id>', methods = ['PATCH'])
def update_customers(id):

    id_req = id
    new_name = request.json['customer_name']
    new_number = request.json['phone_number']

    db.session.query(Customer).filter(Customer.id == id_req).update(dict(customer_name = new_name, phone_number = new_number))
    db.session.commit()

    customer_ = db.session.query(Customer).order_by(Customer.id).limit(15)
    result = customers_schema_many.dump(customer_)
    return jsonify(result)

# Роут производит удаление заданного по id клиента из таблицы customer и связанные с ним по внешнему ключу записи из таблицы orders,
# возвращает обновлённый список записей с сортировкой по id.
@app.route('/customer/<id>', methods = ['DELETE'])
def del_customers(id):

    id_req = id
    db.session.query(Orders).filter(Orders.id_customer == id_req).delete()
    db.session.query(Customer).filter(Customer.id == id_req).delete()
    db.session.commit()

    customer_ = db.session.query(Customer).order_by(Customer.id).limit(15)
    result = customers_schema_many.dump(customer_)
    return jsonify(result)

# Роут выполняет добавление в таблицу customer новую запись, шаблон:
# {
# "customer_name": string
# "phone_number": string
# }
# возвращает обновлённый список записей с сортировкой по id, количество записей ограничено 15
@app.route('/customer', methods = ['PUT'])
def new_customer():

    customer_name_req = request.json['customer_name']
    phone_number_req = request.json['phone_number']

    new_customer = Customer(customer_name_req, phone_number_req)

    db.session.add(new_customer)
    db.session.commit()

    customer_ = db.session.query(Customer).order_by(Customer.id).limit(15)
    result = customers_schema_many.dump(customer_)

    return jsonify(result)

