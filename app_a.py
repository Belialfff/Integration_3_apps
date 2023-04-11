"""Belialfff"""
"""файл для создания подлючения к базе данных и вызова роутов"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DB_TRACK_MODIFICATIONS, DB_URL_a
from flask_marshmallow import Marshmallow


app_a = Flask(__name__)

"""Конфиги для подлючения к бд, содержимое переменных находится во вкладке config"""
app_a.config['SQLALCHEMY_DATABASE_URI'] = DB_URL_a
app_a.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DB_TRACK_MODIFICATIONS

db_a = SQLAlchemy(app_a)

"""Для работы с json форматом используются схемы модуля для сериализации Marshmellow"""
ma_a = Marshmallow(app_a)

"""Импорт всех роутов, лучшего способа их обработать пока не нашёл, исправлю"""

from routes.customers_orders_routes_a import get_customer_orders_by_phone, get_customer_orders_by_name, get_customer_orders
from routes.orders_routes_a import get_orders_all, get_orders, del_orders, new_orders, update_orders
from routes.customers_routes_a import del_customers, get_customers, get_customers_all, new_customer, update_customers
