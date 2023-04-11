"""Belialfff"""
"""файл для создания подлючения к базе данных и вызова роутов"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DB_TRACK_MODIFICATIONS, DB_URL_clients
from flask_marshmallow import Marshmallow


app_clients = Flask(__name__)

"""Конфиги для подлючения к бд, содержимое переменных находится во вкладке config"""
app_clients.config['SQLALCHEMY_DATABASE_URI'] = DB_URL_clients
app_clients.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DB_TRACK_MODIFICATIONS

db_clients = SQLAlchemy(app_clients)

"""Для работы с json форматом используются схемы модуля для сериализации Marshmellow"""
ma_clients = Marshmallow(app_clients)

"""Импорт всех роутов, лучшего способа их обработать пока не нашёл, исправлю"""
from routes.client_routes import get_clients, del_clients, new_clients, update_customer, get_price, get_all_clients



