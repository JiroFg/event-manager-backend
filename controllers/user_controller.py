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
        if not row or row[6] == False:
            self.cursor.close()
            return {
                "error": True,
                "details": "Email or password invalid"
            }
        current_user = UserDisplay(
            user_id=row[0],
            username=row[1],
            email=row[2],
            user_type_id=row[4],
            company_id=row[5],
            is_active=row[6]
        )
        # Validate the current password
        self.cursor.close()
        if not verify_password(password, row[3]):
            return {
                "error": True,
                "details": "Email or password invalid"
            }
        else:
            # generate the token
            token = generate_token({
                "user_id": current_user.user_id,
                "username": current_user.username,
                "email": current_user.email,
                "user_type_id": current_user.user_type_id
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
        query = "INSERT INTO users (username, email, password, user_type_id, is_active) VALUES (%s, %s, %s, 1, 'TRUE')"
        self.cursor.execute(query, (
            new_user.username,
            new_user.email,
            hash_password(new_user.password)
        ))
        rows_affected = self.cursor.rowcount
        self.cursor.close()
        if rows_affected > 0:
            self.conn.commit()
            return {
                "error": False,
                "details": "User created successfully"
            }
        else:
            return {
                "error": True,
                "details": "User couldn't be created"
            }
    
    def create_admin(self, new_user: User):
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
        query = "INSERT INTO users (username, email, password, user_type_id, is_active) VALUES (%s, %s, %s, 2, 'TRUE')"
        self.cursor.execute(query, (
            new_user.username,
            new_user.email,
            hash_password(new_user.password)
        ))
        self.conn.commit()
        rows_affected = self.cursor.rowcount
        self.cursor.close()
        if rows_affected > 0:
            return {
                "error": False,
                "details": "Admin created successfully"
            }
        else:
            return {
                "error": True,
                "details": "Admin couldn't be created"
            }

    def get_all(self):
        result = []
        query = "SELECT user_id, username, email, user_type_id, company_id, is_active FROM users"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            user = UserDisplay(
                user_id=row[0],
                username=row[1],
                email=row[2],
                user_type_id=row[3],
                company_id=row[4],
                is_active=row[5]
            )
            result.append(user)
        self.cursor.close()
        return jsonable_encoder(result)

    def get(self, user_id: int):
        query = "SELECT user_id, username, email, user_type_id, company_id, is_active FROM users WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        row = self.cursor.fetchone()
        if not row:
            return {
                "error": True,
                "details": "User not found"
            }
        user = UserDisplay(
            user_id=row[0],
            username=row[1],
            email=row[2],
            user_type_id=row[3],
            company_id=row[4],
            is_active=row[5]
        )
        self.cursor.close()
        return jsonable_encoder(user)

    def update(self, user_edit: UserEdit):
        # validate if user exists
        query = "SELECT * FROM users WHERE user_id = %s"
        self.cursor.execute(query, (user_edit.user_id,))
        row = self.cursor.fetchone()
        if not row:
            return {
                "error": True,
                "details": "User not found"
            }
        # update user
        query = "UPDATE users SET company_id = COALESCE(%s, company_id), is_active = COALESCE(%s, is_active) WHERE user_id=%s"
        self.cursor.execute(query, (user_edit.company_id, user_edit.is_active, user_edit.user_id))
        self.conn.commit()
        rows_affected = self.cursor.rowcount
        self.cursor.close()
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

    def deactive(self, user_id: int):
        query = "UPDATE users SET is_active = 'FALSE' WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()
        row_affected = self.cursor.rowcount
        if row_affected > 0:
            return {
                "error": False,
                "details": "User deactivate successfully"
            }
        else:
            return {
                "error": True,
                "details": "User couldn't be deactivated"
            }