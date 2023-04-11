"""Belialfff"""
"""Файл запсукает FLASK-приложение на заданном адресе (файл config.py)"""


from app_clients import app_clients
from config import SERVER_HOST, SERVER_PORT_clients, SERVER_DEBUG


app_clients.run(

    host=SERVER_HOST,
    port=SERVER_PORT_clients,
    debug=SERVER_DEBUG
)