from config.db_connection import PostgresConnection
from schemas.user_schema import User
from utils.hashing_helper import hash_password, verify_password
from utils.token_helper import generate_token
from schemas.user_schema import UserDisplay

class UserController():
    def __init__(self):
        self.conn = PostgresConnection.get_instance()

    def login(self, email: str, password: str):
        # Get the user with that email
        cursor = self.conn.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        if not row:
            cursor.close()
            return {
                "error": True,
                "details": "Email or password invalid"
            }
        current_user = UserDisplay(
            user_id=row[0],
            username=row[1],
            email=row[2],
            password=row[3],
            company_id=row[4]
        )
        # Validate the current password
        if not verify_password(password, current_user.password):
            cursor.close()
            return {
                "error": True,
                "details": "Email or password invalid"
            }
        else:
            # generate the token
            token = generate_token({
                "user_id": current_user.user_id,
                "username": current_user.username,
                "email": current_user.email
            })
            return {
                "access_token": token,
                "token_type": "bearer"
            }

    def create(self, new_user: User):
        cursor = self.conn.cursor()
        # Validate if user with the email already exist
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (new_user.email,))
        row = cursor.fetchone()
        if row:
            return {
                "error": True,
                "details": "Email already registered"
            }
        # Create the new user
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (
            new_user.username,
            new_user.email,
            hash_password(new_user.password)
        ))
        self.conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        if(rows_affected > 0):
            return {
                "error": False,
                "details": "User created successfully"
            }
        else:
            return {
                "error": True,
                "details": "User couldn't be created"
            }

    def get_all(self):
        pass

    def get(self, user_id: int):
        pass

    def update(self):
        pass

    def delete(self):
        pass