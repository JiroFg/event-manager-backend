from fastapi.encoders import jsonable_encoder
from config.db_connection import PostgresConnection
from schemas.product_schema import Product, ProductDisplay, ProductEdit

class ProductController():
    def __init__(self):
        self.conn = PostgresConnection.get_instance()
        self.cursor = self.conn.cursor()

    def create(self, new_product: Product):
        # check if the owner exists
        query = "SELECT * FROM users WHERE user_id = %s"
        self.cursor.execute(query, (new_product.owner_id,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Invalid user"
            }
        # add product
        query = "INSERT INTO products (name, description, img_url, owner_id) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (new_product.name, new_product.description, new_product.img_url, new_product.owner_id))
        affected_row = self.cursor.rowcount
        self.cursor.close()
        if affected_row > 0:
            self.conn.commit()
            return {
                "error": False,
                "details": "Product created successfully"
            }
        else:
            return {
                "error": True,
                "details": "Product couldn't be created"
            }
    
    def get_products_by_event(self, event_id: int):
        result = []
        query = "SELECT product_id, name, description, img_url, owner_id FROM products JOIN user_event_participation ON products.owner_id = user_event_participation.user_id WHERE user_event_participation.event_id = %s"
        self.cursor.execute(query, (event_id,))
        rows = self.cursor.fetchall()
        for row in rows:
            product = ProductDisplay(
                product_id=row[0],
                name=row[1],
                description=row[2],
                img_url=row[3],
                owner_id=row[4]
            )
            result.append(product)
        self.cursor.close()
        return jsonable_encoder(result)
    
    def get_products_by_user(self, user_id: int):
        result = []
        query = "SELECT * FROM products WHERE owner_id = %s"
        self.cursor.execute(query, (user_id,))
        rows = self.cursor.fetchall()
        for row in rows: 
            product = ProductDisplay(
                product_id=row[0],
                name=row[1],
                description=row[2],
                img_url=row[3],
                owner_id=row[4]
            )
            result.append(product)
        self.cursor.close()
        return jsonable_encoder(result)
    
    def update_product(self, product_edit: ProductEdit):
        # check if product id is valid
        query = "SELECT * FROM products WHERE product_id = %s"
        self.cursor.execute(query, (product_edit.product_id,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Product not found"
            }
        # check if user is valid
        query = "SELECT * FROM users WHERE user_id = %s"
        self.cursor.execute(query, (product_edit.owner_id,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Invalid user"
            }
        # update product
        query = "UPDATE products SET name = COALESCE(%s, name), description = COALESCE(%s, description), img_url = COALESCE(%s, img_url), owner_id = COALESCE(%s, owner_id) WHERE product_id = %s"
        self.cursor.execute(query, (product_edit.name, product_edit.description, product_edit.img_url, product_edit.owner_id, product_edit.product_id))
        affected_row = self.cursor.rowcount
        self.cursor.close()
        if affected_row > 0:
            self.conn.commit()
            return {
                "error": False,
                "details": "Product updated successfully"
            }
        else:
            return {
                "error": True,
                "details": "Product couldn't be updated"
            }
