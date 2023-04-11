"""Belialfff"""
"""Файл запсукает FLASK-приложение на заданном адресе (файл config.py)"""


from app_b import app_b
from config import SERVER_HOST, SERVER_PORT_b, SERVER_DEBUG


app_b.run(

    host=SERVER_HOST,
    port=SERVER_PORT_b,
    debug=SERVER_DEBUG
)
