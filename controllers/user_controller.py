from fastapi.encoders import jsonable_encoder
from config.db_connection import PostgresConnection
from schemas.user_schema import User, UserEdit
from utils.hashing_helper import hash_password, verify_password
from utils.token_helper import generate_token
from schemas.user_schema import UserDisplay

class UserController():
    def __init__(self):
        self.conn = PostgresConnection.get_instance()
        self.cursor = self.conn.cursor()

    def login(self, email: str, password: str):
        # Get the user with that email
        query = "SELECT * FROM users WHERE email = %s"
        self.cursor.execute(query, (email,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.close()
            return {
                "error": True,
                "details": "Email or password invalid"
            }
        current_user = UserDisplay(
            user_id=row[0],
            username=row[1],
            email=row[2],
            company_id=row[4]
        )
        # Validate the current password
        if not verify_password(password, row[3]):
            self.cursor.close()
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
        # Validate if user with the email already exist
        query = "SELECT * FROM users WHERE email = %s"
        self.cursor.execute(query, (new_user.email,))
        row = self.cursor.fetchone()
        if row:
            return {
                "error": True,
                "details": "Email already registered"
            }
        # Create the new user
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (
            new_user.username,
            new_user.email,
            hash_password(new_user.password)
        ))
        self.conn.commit()
        rows_affected = self.cursor.rowcount
        self.cursor.close()
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
        result = []
        query = "SELECT user_id, username, email, company_id FROM users"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
            user = UserDisplay(
                user_id=row[0],
                username=row[1],
                email=row[2],
                company_id=row[3]
            )
            result.append(user)
        self.cursor.close()
        return jsonable_encoder(result)

    def get(self, user_id: int):
        query = "SELECT user_id, username, email, company_id FROM users WHERE user_id=%s"
        self.cursor.execute(query, (user_id,))
        row = self.cursor.fetchone()
        user = UserDisplay(
            user_id=row[0],
            username=row[1],
            email=row[2],
            company_id=row[3]
        )
        return jsonable_encoder(user)

    def update(self, user_edit: UserEdit):
        query = "UPDATE users SET company_id = COALESCE(%s, company_id) WHERE user_id=%s"
        self.cursor.execute(query, (user_edit.company_id, user_edit.user_id))
        rows_affected = self.cursor.rowcount
        if rows_affected > 0:
            return {
                "error": False,
                "details": "User updated successfully"
            }
        else:
            return {
                "error": True,
                "details": "User couldn't be updated"
            }

    def delete(self):
        pass