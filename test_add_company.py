import requests
import json

def test_add_company():
    """测试新增局点功能"""
    # 测试数据
    company_data = {
        "name": "测试新增局点",
        "description": "这是一个测试用的新增局点",
        "tenantId": 2  # 测试电信
    }
    
    # 发起请求
    url = "http://localhost:8080/ces/company/add"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=company_data, headers=headers)
        
        # 输出状态码
        print(f"状态码: {response.status_code}")
        
        # 尝试解析JSON响应
        try:
            result = response.json()
            print("响应内容:")
            print(json.dumps(result, indent=4, ensure_ascii=False))
            
            # 检查响应码
            if result.get("code") == "00000":
                print("\n✅ 测试成功: 局点添加成功")
                print(f"新增局点ID: {result.get('data', {}).get('id')}")
                print(f"局点名称: {result.get('data', {}).get('name')}")
                print(f"所属租户: {result.get('data', {}).get('tenantId')}")
            else:
                print(f"\n❌ 测试失败: {result.get('msg')}")
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")

def test_company_list_page():
    """测试分页查询局点列表"""
    # 测试数据
    query_data = {
        "companyName": "",
        "pageNo": 1,
        "pageSize": 10,
        "tenantId": 0  # 查询所有租户
    }
    
    # 发起请求
    url = "http://localhost:8080/ces/company/list/page"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=query_data, headers=headers)
        
        # 输出状态码
        print(f"状态码: {response.status_code}")
        
        # 尝试解析JSON响应
        try:
            result = response.json()
            print("响应内容:")
            print(json.dumps(result, indent=4, ensure_ascii=False))
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    # 测试新增局点
    print("===== 测试新增局点 =====")
    test_add_company()
    
    # 测试分页查询
    print("\n===== 测试分页查询局点列表 =====")
    test_company_list_page() 