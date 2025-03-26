import requests
import json
import random
import time

# 设置基础URL
BASE_URL = "http://localhost:8000"

def test_role_add():
    """测试添加角色"""
    # 随机生成角色名称，防止重名
    role_name = f"测试角色-{random.randint(1000, 9999)}"
    
    # 准备请求数据
    data = {
        "name": role_name,
        "description": "这是一个测试角色描述"
    }
    
    # 发送请求
    response = requests.post(f"{BASE_URL}/ces/role/add", json=data)
    
    # 输出结果
    print("测试添加角色:")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

    # 返回创建的角色名称，以便后续测试使用
    return role_name

def test_role_list():
    """测试获取角色列表"""
    # 发送请求
    response = requests.get(f"{BASE_URL}/ces/role/list")
    
    # 输出结果
    print("测试获取角色列表:")
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()
    
    # 返回角色列表，以便后续测试使用
    resp_data = response.json()
    if resp_data.get("code") == "00000":
        return resp_data.get("data", [])
    return []

def test_role_page(role_name=None):
    """测试角色分页查询"""
    # 准备请求数据
    data = {
        "name": role_name if role_name else "",
        "pageNo": 1,
        "pageSize": 10
    }
    
    # 发送请求
    response = requests.post(f"{BASE_URL}/ces/role/list/page", json=data)
    
    # 输出结果
    print("测试角色分页查询:")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()
    
    # 返回角色数据，以便后续测试使用
    resp_data = response.json()
    if resp_data.get("code") == "00000":
        return resp_data.get("data", {}).get("records", [])
    return []

def test_role_modify(role_id, new_name, new_description):
    """测试修改角色"""
    # 准备请求数据
    data = {
        "id": role_id,
        "name": new_name,
        "description": new_description
    }
    
    # 发送请求
    response = requests.post(f"{BASE_URL}/ces/role/modify", json=data)
    
    # 输出结果
    print("测试修改角色:")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_role_delete(role_id):
    """测试删除角色"""
    # 发送请求
    response = requests.delete(f"{BASE_URL}/ces/role/delete?id={role_id}")
    
    # 输出结果
    print("测试删除角色:")
    print(f"删除角色ID: {role_id}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def main():
    print("======== 开始测试角色管理API ========")
    
    # 测试添加角色
    role_name = test_role_add()
    
    # 等待一会以确保数据库更新
    time.sleep(1)
    
    # 测试角色列表
    roles = test_role_list()
    
    # 测试角色分页查询（搜索新添加的角色）
    role_records = test_role_page(role_name)
    
    # 如果找到新添加的角色，测试修改和删除
    if role_records:
        role_id = role_records[0]["id"]
        
        # 测试修改角色
        new_name = f"修改后的角色-{random.randint(1000, 9999)}"
        test_role_modify(role_id, new_name, "这是修改后的角色描述")
        
        # 等待一会以确保数据库更新
        time.sleep(1)
        
        # 再次查询，验证修改效果
        test_role_page(new_name)
        
        # 测试删除角色
        test_role_delete(role_id)
        
        # 等待一会以确保数据库更新
        time.sleep(1)
        
        # 再次查询，验证删除效果
        test_role_page(new_name)
    
    print("======== 角色管理API测试完成 ========")

if __name__ == "__main__":
    main() 