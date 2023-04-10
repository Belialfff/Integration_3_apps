"""Belialfff"""
"""Файл со схемами таблиц баз данных"""


from app_b import db_b


class Customer_b(db_b.Model):
    __tablename__ = 'customers'

    id = db_b.Column(db_b.Integer, primary_key=True, autoincrement=True)
    customer_name = db_b.Column(db_b.String())
    phone_number = db_b.Column(db_b.String())

    def __init__(self, customer_name, phone_number):
        self.customer_name = customer_name
        self.phone_number = phone_number

    def __repr__(self):
        return f""

class Orders_b(db_b.Model):
    __tablename__ = 'orders'

    id = db_b.Column(db_b.Integer, primary_key=True, autoincrement=True)
    clin_type = db_b.Column(db_b.String())
    price = db_b.Column(db_b.Integer())
    id_customer = db_b.Column(db_b.Integer, db_b.ForeignKey(Customer_b.id))

    def __init__(self, clin_type, price, id_customer):
        self.clin_type = clin_type
        self.price = price
        self.id_customer = id_customer

    def __repr__(self):
        return f""
