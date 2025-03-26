import requests
import json

def test_grid_list_all():
    """测试查询所有网格"""
    url = "http://localhost:8080/ces/grid/list"
    payload = {
        "companyId": 0
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
                
                # 打印网格信息
                if grids:
                    print("\n网格列表:")
                    for i, grid in enumerate(grids, 1):
                        print(f"{i}. ID: {grid.get('id')}, 名称: {grid.get('name')}")
            else:
                print(f"\n❌ 测试失败: {data.get('msg')}")
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")

def test_grid_list_by_company(company_id):
    """测试查询特定局点的网格"""
    url = "http://localhost:8080/ces/grid/list"
    payload = {
        "companyId": company_id
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
                print(f"\n✅ 测试成功: 局点 {company_id} 下有 {len(grids)} 个网格")
                
                # 打印网格信息
                if grids:
                    print("\n网格列表:")
                    for i, grid in enumerate(grids, 1):
                        print(f"{i}. ID: {grid.get('id')}, 名称: {grid.get('name')}")
            else:
                print(f"\n❌ 测试失败: {data.get('msg')}")
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    # 测试查询所有网格
    print("===== 测试查询所有网格 =====")
    test_grid_list_all()
    
    # 测试查询特定局点的网格
    print("\n===== 测试查询局点1的网格 =====")
    test_grid_list_by_company(1)
    
    print("\n===== 测试查询局点2的网格 =====")
    test_grid_list_by_company(2)
    
    print("\n===== 测试查询局点3的网格 =====")
    test_grid_list_by_company(3)
    
    print("\n===== 测试查询不存在的局点 =====")
    test_grid_list_by_company(999) 