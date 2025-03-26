import requests
import json

def test_tenant_list():
    url = "http://localhost:8080/ces/tenant/list"
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers)
    print("\n运营商列表查询测试:")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("Response:")
        print(json.dumps(data, indent=4, ensure_ascii=False))
    else:
        print(f"Error Response: {response.text}")

if __name__ == "__main__":
    test_tenant_list() 