from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import DB_TRACK_MODIFICATIONS
from flask_marshmallow import Marshmallow


app = Flask(__name__)


#Путь к базе данных postgresql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:28032@localhost:5432/Technic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = DB_TRACK_MODIFICATIONS

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Импорт роутов
from orders_routes import get_orders, get_orders_all, del_orders, new_orders, update_orders
from customers_routes import get_customers, get_customers_all, del_customers, update_customers, new_customer
from customers_orders_routes import get_customer_orders, get_customer_orders_by_name









