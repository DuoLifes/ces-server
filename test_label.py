import requests
import json
import random
import time

# 设置基础URL
BASE_URL = "http://localhost:8000"

def test_label_add(label_type=1):
    """测试添加标签"""
    # 随机生成标签名称，防止重名
    label_name = f"测试标签-{random.randint(1000, 9999)}"
    
    # 准备请求数据
    data = {
        "name": label_name,
        "type": label_type
    }
    
    # 发送请求
    response = requests.post(f"{BASE_URL}/ces/label/add", json=data)
    
    # 输出结果
    print("测试添加标签:")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

    # 返回创建的标签名称，以便后续测试使用
    return label_name

def test_label_page(name="", company_id=0, label_type=0):
    """测试标签分页查询"""
    # 准备请求数据
    data = {
        "name": name,
        "companyId": company_id,
        "pageNo": 1,
        "pageSize": 10,
        "type": label_type
    }
    
    # 发送请求
    response = requests.post(f"{BASE_URL}/ces/label/list/page", json=data)
    
    # 输出结果
    print("测试标签分页查询:")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()
    
    # 返回标签数据，以便后续测试使用
    resp_data = response.json()
    if resp_data.get("code") == "00000":
        return resp_data.get("data", {}).get("records", [])
    return []

def test_label_modify(label_id, new_name, new_type):
    """测试修改标签"""
    # 准备请求数据
    data = {
        "id": label_id,
        "name": new_name,
        "type": new_type
    }
    
    # 发送请求
    response = requests.post(f"{BASE_URL}/ces/label/modify", json=data)
    
    # 输出结果
    print("测试修改标签:")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_label_configure_company(label_id, company_list):
    """测试配置标签局点"""
    # 准备请求数据
    data = {
        "id": label_id,
        "companyList": company_list
    }
    
    # 发送请求
    response = requests.post(f"{BASE_URL}/ces/label/configure/label_company", json=data)
    
    # 输出结果
    print("测试配置标签局点:")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_label_delete(label_id):
    """测试删除标签"""
    # 发送请求
    response = requests.delete(f"{BASE_URL}/ces/label/delete?id={label_id}")
    
    # 输出结果
    print("测试删除标签:")
    print(f"删除标签ID: {label_id}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def get_company_list():
    """获取可用的局点列表"""
    response = requests.get(f"{BASE_URL}/ces/company/list")
    
    if response.status_code == 200:
        resp_data = response.json()
        if resp_data.get("code") == "00000":
            return resp_data.get("data", [])
    
    return []

def main():
    print("======== 开始测试标签管理API ========")
    
    # 获取可用的局点列表
    companies = get_company_list()
    company_ids = [company.get("id") for company in companies]
    
    # 测试添加基础标签
    label_name_1 = test_label_add(label_type=1)
    
    # 测试添加高级标签
    label_name_2 = test_label_add(label_type=2)
    
    # 等待一会以确保数据库更新
    time.sleep(1)
    
    # 测试标签分页查询（查询所有标签）
    test_label_page()
    
    # 测试标签分页查询（按名称查询）
    label_records_1 = test_label_page(name=label_name_1)
    label_records_2 = test_label_page(name=label_name_2)
    
    # 测试标签分页查询（按类型查询）
    test_label_page(label_type=1)
    test_label_page(label_type=2)
    
    # 如果找到新添加的标签，测试修改和配置局点
    if label_records_1:
        label_id = label_records_1[0]["id"]
        
        # 如果有可用的局点，测试配置标签局点
        if company_ids:
            # 随机选择1-3个局点
            selected_company_ids = random.sample(company_ids, min(3, len(company_ids)))
            test_label_configure_company(label_id, selected_company_ids)
            
            # 等待一会以确保数据库更新
            time.sleep(1)
            
            # 测试按局点ID查询标签
            if selected_company_ids:
                test_label_page(company_id=selected_company_ids[0])
        
        # 测试修改标签
        new_name = f"修改后的标签-{random.randint(1000, 9999)}"
        test_label_modify(label_id, new_name, 1)
        
        # 等待一会以确保数据库更新
        time.sleep(1)
        
        # 再次查询，验证修改效果
        test_label_page(name=new_name)
        
        # 测试删除标签
        test_label_delete(label_id)
        
        # 等待一会以确保数据库更新
        time.sleep(1)
        
        # 再次查询，验证删除效果
        test_label_page(name=new_name)
    
    # 如果找到新添加的高级标签，测试删除
    if label_records_2:
        label_id = label_records_2[0]["id"]
        test_label_delete(label_id)
    
    print("======== 标签管理API测试完成 ========")

if __name__ == "__main__":
    main() 