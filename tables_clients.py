"""Belialfff"""
"""Файл со схемами таблиц баз данных"""


from app_clients import db_clients


class Clients(db_clients.Model):
    __tablename__ = 'clients'

    id = db_clients.Column(db_clients.Integer, primary_key=True, autoincrement=True)
    customer_name = db_clients.Column(db_clients.String())
    phone_number = db_clients.Column(db_clients.String())
    price = db_clients.Column(db_clients.Integer())

    def __init__(self, customer_name, phone_number, price):
        self.customer_name = customer_name
        self.phone_number = phone_number
        self.price = price

    def __repr__(self):
        return f""
