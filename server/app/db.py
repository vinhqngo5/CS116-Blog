import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

config = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': '127.0.0.1',
    'database': 'blog',
    'raise_on_warnings': True
}

conn = None

def connect_db():
    try:
        global conn
        conn = mysql.connector.connect(**config)

        print("Connected to database")

    except Exception as e:
        print("Cannot connect to database...")
        print(e)
        exit(1)

def get_db():
    return conn
