"""Belialfff"""
"""Файл со схемами таблиц баз данных"""


from app import db


class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String())
    phone_number = db.Column(db.String())

    def __init__(self, customer_name, phone_number):
        self.customer_name = customer_name
        self.phone_number = phone_number

    def __repr__(self):
        return f""

class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    technic = db.Column(db.String())
    price = db.Column(db.Integer())
    id_customer = db.Column(db.Integer, db.ForeignKey(Customer.id))

    def __init__(self, technic, price, id_customer):
        self.technic = technic
        self.price = price
        self.id_customer = id_customer

    def __repr__(self):
        return f""
