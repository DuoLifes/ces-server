import requests

def test_login(username, password):
    url = "http://localhost:8080/ces/sys/account/login"
    data = {
        "username": username,
        "password": password
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"\n测试登录 - 用户名: {username}, 密码: {password}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    # 测试正确的用户名和密码
    test_login("zxjy", "zxjy")
    
    # 测试错误的用户名和密码
    test_login("aaa", "aaa") 