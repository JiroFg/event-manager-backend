import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

class PostgresConnection:

    _instance = None

    @staticmethod
    def get_instance():
        if PostgresConnection._instance == None:
            PostgresConnection()
        return PostgresConnection._instance
    
    def __init__(self):
        if PostgresConnection._instance != None:
            raise Exception("Connection already exist")
        else:
            PostgresConnection._instance = psycopg2.connect(database=os.getenv("POSTGRES_DB"), user=os.getenv("POSTGRES_USER"), password=os.getenv("POSTGRES_PASSWORD"), host=os.getenv("POSTGRES_HOST"), port=os.getenv("POSTGRES_PORT"))