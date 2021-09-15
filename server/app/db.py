import os
from flask import globals
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
        conn = mysql.connector.connect(**config)
        print("Connected to database")
        cursor = conn.cursor()
        return cursor
    except:
        print()
        print("Cannot connect to database...")
        exit(1)



    

    
    