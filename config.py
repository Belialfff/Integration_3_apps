"""Belialfff"""
"""Конфигурация подлючения базы данных к серверу"""

"""Подключение осуществляется по шаблону 'your database+sqlalchemy database driver://user:password@host:port/database
В переменной DB_URL пример подключения к базе данных mySQL, для создания приложен скрипт в файле 'SQL-Scripts' 
Для подключения к другой базе данных нужен соответствующий драйвер, в комментариях находится 
пример с драйвером для подключения к Postgresql"""

DB_URL = 'mysql+pymysql://root:28032@localhost:3306/technic'
# 'postgresql+psycopg2://postgres:28032@localhost:5432/Technic'
DB_TRACK_MODIFICATIONS = True

"""Используемые адрес и порт"""
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000
SERVER_DEBUG = True
