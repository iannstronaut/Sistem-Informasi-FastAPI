from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello You!"}

def test_add_user():

    response = client.post("/user", json={
        "username"  : "budiono",
        "email"     : "budionos3@gmail.com",
        "password"  : "budiono12345"
    })

    print(response.status_code)
    print(response.json())
    
    assert response.status_code == 201
    
    assert response.json() == {"message": "User created successfully", "user": "budiono"}

def test_get_user_by_id():
    response = client.get("/user/1")
    assert response.status_code == 200
    assert response.json() == {"user_id": 1, "username": "budiono", "email" : "budionos3@gmail.com"}

def test_update_user_by_id():

    response = client.put("/user/1", json={
        "username"  : "siregar",
        "email"     : "siregar@gmail.com",
        "password"  : "budiono12345"
    })

    assert response.status_code == 200
    assert response.json() == { "message": "User updated successfully",
        "user": {
            "email": "siregar@gmail.com",
            "username": "siregar",
        }
    }

def test_delete_user_by_id():
    response = client.delete("/user/1")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}

