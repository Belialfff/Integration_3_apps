"""Belialfff"""
"""Файл запсукает FLASK-приложение на заданном адресе (файл config.py)"""


from app import app
from config import SERVER_HOST, SERVER_PORT, SERVER_DEBUG


app.run(

    host=SERVER_HOST,
    port=SERVER_PORT,
    debug=SERVER_DEBUG
)