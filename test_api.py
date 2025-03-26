import requests
import json

BASE_URL = "http://localhost:8000"

def test_register():
    url = f"{BASE_URL}/register"
    data = {
        "username": "testuser2",
        "password": "password123"
    }
    response = requests.post(url, json=data)
    print("\n注册测试:")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    return response.json()

def test_login():
    url = f"{BASE_URL}/token"
    data = {
        "username": "testuser2",
        "password": "password123"
    }
    response = requests.post(url, data=data)
    print("\n登录测试:")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")

if __name__ == "__main__":
    test_register()
    test_login() 