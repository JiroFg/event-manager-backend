import bcrypt

def hash_password(password: str):
    hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    print(hashed.decode())
    return hashed.decode()

def verify_password(password, hashed_password):
    return bcrypt.checkpw(str.encode(password), str.encode(hashed_password))