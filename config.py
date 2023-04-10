"""Belialfff"""
"""Конфигурация подлючения базы данных к серверу"""

"""Подключение осуществляется по шаблону 'your database+sqlalchemy database driver://user:password@host:port/database
В переменной DB_URL пример подключения к базе данных mySQL, для создания приложен скрипт в файле 'SQL-Scripts' 
Для подключения к другой базе данных нужен соответствующий драйвер, в комментариях находится 
пример с драйвером для подключения к Postgresql"""

#DB_URL = 'mysql+pymysql://root:28032@localhost:3306/technic'
DB_URL_a = 'postgresql+psycopg2://postgres:28032@localhost:5432/Technic_a'
DB_URL_b = 'postgresql+psycopg2://postgres:28032@localhost:5432/Clining_b'
DB_URL_clients = 'postgresql+psycopg2://postgres:28032@localhost:5432/Clients'
DB_TRACK_MODIFICATIONS = True

"""Используемые адрес и порт"""
SERVER_HOST = '127.0.0.1'
SERVER_PORT_a = 8000
SERVER_PORT_b = 8001
SERVER_PORT_clients = 8002
SERVER_DEBUG = True
