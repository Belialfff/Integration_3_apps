"""Belialfff"""
"""файл для создания подлючения к базе данных и вызова роутов"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DB_TRACK_MODIFICATIONS, DB_URL_b
from flask_marshmallow import Marshmallow


app_b = Flask(__name__)

"""Конфиги для подлючения к бд, содержимое переменных находится во вкладке config"""
app_b.config['SQLALCHEMY_DATABASE_URI'] = DB_URL_b
app_b.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DB_TRACK_MODIFICATIONS

db_b = SQLAlchemy(app_b)

"""Для работы с json форматом используются схемы модуля для сериализации Marshmellow"""
ma_b = Marshmallow(app_b)

"""Импорт всех роутов, лучшего способа их обработать пока не нашёл, исправлю"""

from routes.customers_orders_routes_b import get_customer_orders_by_phone, get_customer_orders_by_name, get_customer_orders
from routes.orders_routes_b import get_orders_all, get_orders, del_orders, new_orders, update_orders
from routes.customers_routes_b import del_customers, get_customers, get_customers_all, new_customer, update_customers
