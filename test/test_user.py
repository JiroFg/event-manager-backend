from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    body = {
        "email": "changuito@gmail.com",
        "password": "Changuito125",
        "username": "changuito"
    }
    response = client.post("/user/", json=body)
    assert response.status_code == 200
    assert response.json() == {
        "error": False,
        "details": "User created successfully"
    }

def test_create_user_already_exists():
    body = {
        "email": "changuito@gmail.com",
        "password": "Changuito125",
        "username": "changuito"
    }
    response = client.post("/user/", json=body)
    assert response.status_code == 200
    assert response.json() == {
        "error": True,
        "details": "Email already registered"
    }

# aux function
def login_user():
    form = {
        "username": "changuito@gmail.com",
        "password": "Changuito125"
    }
    response = client.post("/login", data=form)
    return response

def login_admin_user():
    form = {
        "username":"tilin@gmail.com",
        "password":"Tilin125"
    }
    response = client.post("/login", data=form)
    return response

def test_login_user():
    response = login_user()
    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "bearer"

# admin
def test_create_admin():
    response = login_admin_user()
    json = response.json()
    body = {
        "email": "testadmin@gmail.com",
        "password": "Testadmin125",
        "username": "testadmin"
    }
    headers = {
        "Authorization": f"{json.get("token_type")} {json.get("access_token")}"
    }
    response = client.post("/user/admin/", json=body, headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "error": False,
        "details": "Admin created successfully"
    }

# def test_update_user():
#     body = {}
#     response = client.post()
#     body = {
#         "user_id": 0,
#         "company_id": 0,
#         "is_active": True
#     }
