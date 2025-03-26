import requests
import json

def test_tenant_list():
    """测试运营商列表查询接口"""
    url = "http://localhost:8080/ces/tenant/list"
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # 发送POST请求
        response = requests.post(url, headers=headers)
        
        # 打印状态码
        print(f"状态码: {response.status_code}")
        
        # 尝试解析JSON响应
        try:
            data = response.json()
            print(f"响应内容: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # 检查响应码
            if data.get("code") == "00000":
                tenants = data.get("data", [])
                print(f"\n✅ 测试成功: 获取到 {len(tenants)} 个运营商")
                
                # 打印运营商信息
                if tenants:
                    print("\n运营商列表:")
                    for i, tenant in enumerate(tenants, 1):
                        print(f"{i}. ID: {tenant.get('id')}, 名称: {tenant.get('name')}")
            else:
                print(f"\n❌ 测试失败: {data.get('msg')}")
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")

def test_company_list():
    """测试局点列表查询接口"""
    url = "http://localhost:8080/ces/company/list"
    payload = {
        "tenantId": 0  # 查询所有租户的局点
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # 发送POST请求
        response = requests.post(url, json=payload, headers=headers)
        
        # 打印状态码
        print(f"状态码: {response.status_code}")
        
        # 尝试解析JSON响应
        try:
            data = response.json()
            print(f"响应内容: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # 检查响应码
            if data.get("code") == "00000":
                companies = data.get("data", [])
                print(f"\n✅ 测试成功: 获取到 {len(companies)} 个局点")
                
                # 打印局点信息
                if companies:
                    print("\n局点列表:")
                    for i, company in enumerate(companies, 1):
                        print(f"{i}. ID: {company.get('id')}, 名称: {company.get('name')}")
            else:
                print(f"\n❌ 测试失败: {data.get('msg')}")
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")

def test_grid_list():
    """测试网格列表查询接口"""
    url = "http://localhost:8080/ces/grid/list"
    payload = {
        "companyId": 0  # 查询所有局点的网格
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # 发送POST请求
        response = requests.post(url, json=payload, headers=headers)
        
        # 打印状态码
        print(f"状态码: {response.status_code}")
        
        # 尝试解析JSON响应
        try:
            data = response.json()
            print(f"响应内容: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # 检查响应码
            if data.get("code") == "00000":
                grids = data.get("data", [])
                print(f"\n✅ 测试成功: 获取到 {len(grids)} 个网格")
                
                # 打印前10个网格信息
                if grids:
                    print("\n网格列表(前10个):")
                    for i, grid in enumerate(grids[:10], 1):
                        print(f"{i}. ID: {grid.get('id')}, 名称: {grid.get('name')}")
                    
                    if len(grids) > 10:
                        print(f"... 还有 {len(grids) - 10} 个网格未显示")
            else:
                print(f"\n❌ 测试失败: {data.get('msg')}")
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    # 测试查询运营商列表
    print("===== 测试运营商列表查询 =====")
    test_tenant_list()
    
    # 测试查询局点列表
    print("\n===== 测试局点列表查询 =====")
    test_company_list()
    
    # 测试查询网格列表
    print("\n===== 测试网格列表查询 =====")
    test_grid_list() 