from config.db_connection import PostgresConnection
from schemas.user_type_schema import UserTypeDisplay
from schemas.country_schema import CountryDisplay
from schemas.state_schema import StateDisplay
from fastapi.encoders import jsonable_encoder

class CatalogController():
    def __init__(self):
        self.conn = PostgresConnection.get_instance()
        self.cursor = self.conn.cursor()
    
    def get_all(self, table: str, result_class: object):
        result = []
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            class_instance = result_class(**{key: row[i] for i, key in enumerate(result_class.__fields__.keys())})
            result.append(class_instance)
        self.cursor.close()
        return jsonable_encoder(result)
    
    def get_user_types(self):
        return self.get_all(
            "user_types",
            UserTypeDisplay
        )
    
    def get_countries(self):
        return self.get_all(
            "countries",
            CountryDisplay
        )
    
    def get_states(self):
        return self.get_all(
            "states",
            StateDisplay
        )