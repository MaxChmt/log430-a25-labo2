"""
Database connections
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import time
import mysql.connector
import redis
import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()

def get_mysql_conn():
    """Get a MySQL connection using env variables"""
    return mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASS,
        database=config.DB_NAME
    )

def get_redis_conn():
    """Get a Redis connection using env variables"""
    session = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True)
    return session

def get_sqlalchemy_session():
    """Get an SQLAlchemy ORM session using env variables"""
    connection_string = f'mysql+mysqlconnector://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    return Session()

def wait_for_mysql(max_retries=5, delay=3):
    for attempt in range(1, max_retries + 1):
        try:
            conn = get_mysql_conn()
            conn.close()
            print("[DEBUG] MySQL prêt")
            return
        except Exception as e:
            print(f"[DEBUG] Tentative {attempt}: MySQL pas prêt ({e}), retry dans {delay}s")
            time.sleep(delay)
    raise Exception("Impossible de se connecter à MySQL après plusieurs tentatives")

