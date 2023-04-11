"""Belialfff"""
"""Файл запсукает FLASK-приложение на заданном адресе (файл config.py)"""


from app_a import app_a
from config import SERVER_HOST, SERVER_PORT_a, SERVER_DEBUG


app_a.run(

    host=SERVER_HOST,
    port=SERVER_PORT_a,
    debug=SERVER_DEBUG
)
