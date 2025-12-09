import requests

def test_auth():
    # 1. Register
    reg_url = "http://localhost:8000/users/"
    payload = {"email": "py_test_user@example.com", "password": "password123"}
    try:
        r = requests.post(reg_url, json=payload)
        print(f"Register Status: {r.status_code}")
        print(f"Register Response: {r.text}")
    except Exception as e:
        print(f"Register Failed: {e}")

    # 2. Login
    login_url = "http://localhost:8000/token"
    login_data = {"username": "py_test_user@example.com", "password": "password123"}
    try:
        r = requests.post(login_url, data=login_data)
        print(f"Login Status: {r.status_code}")
        if r.status_code == 200:
            print("Login Success! Token received.")
        else:
             print(f"Login Response: {r.text}")
    except Exception as e:
        print(f"Login Failed: {e}")

if __name__ == "__main__":
    test_auth()
