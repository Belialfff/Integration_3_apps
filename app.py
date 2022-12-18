"""Belialfff"""
"""файл для создания подлючения к базе данных и вызова роутов"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DB_TRACK_MODIFICATIONS, DB_URL
from flask_marshmallow import Marshmallow


app = Flask(__name__)

"""Конфиги для подлючения к бд, содержимое переменных находится во вкладке config"""
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DB_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

"""Для работы с json форматом используются схемы модуля для сериализации Marshmellow"""
ma = Marshmallow(app)

"""Импорт всех роутов, лучшего способа их обработать пока не нашёл, исправлю"""
from orders_routes import get_orders, get_orders_all, del_orders, new_orders, update_orders
from customers_routes import get_customers, get_customers_all, del_customers, update_customers, new_customer
from customers_orders_routes import get_customer_orders, get_customer_orders_by_name









