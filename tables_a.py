"""Belialfff"""
"""Файл со схемами таблиц баз данных"""


from app_a import db_a


class Customer_a(db_a.Model):
    __tablename__ = 'customers'

    id = db_a.Column(db_a.Integer, primary_key=True, autoincrement=True)
    customer_name = db_a.Column(db_a.String())
    phone_number = db_a.Column(db_a.String())

    def __init__(self, customer_name, phone_number):
        self.customer_name = customer_name
        self.phone_number = phone_number

    def __repr__(self):
        return f""

class Orders_a(db_a.Model):
    __tablename__ = 'orders'

    id = db_a.Column(db_a.Integer, primary_key=True, autoincrement=True)
    technic = db_a.Column(db_a.String())
    price = db_a.Column(db_a.Integer())
    id_customer = db_a.Column(db_a.Integer, db_a.ForeignKey(Customer_a.id))

    def __init__(self, technic, price, id_customer):
        self.technic = technic
        self.price = price
        self.id_customer = id_customer

    def __repr__(self):
        return f""
