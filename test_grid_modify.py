import requests
import json

def test_grid_modify():
    """测试网格修改接口"""
    url = "http://localhost:8080/ces/grid/modify"
    headers = {
        "Content-Type": "application/json"
    }
    
    # 首先调用网格列表接口获取一个现有的网格ID
    existing_grid = get_existing_grid()
    if not existing_grid:
        print("❌ 无法获取现有网格进行测试，请确保数据库中有网格数据")
        return
    
    # 准备测试数据
    grid_id = existing_grid.get("id")
    original_company_id = existing_grid.get("companyId")
    
    # 测试1: 仅修改网格名称
    print("\n===== 测试1: 仅修改网格名称 =====")
    payload1 = {
        "id": grid_id,
        "name": f"修改后的网格名称-测试-{grid_id}"
    }
    perform_test(url, headers, payload1)
    
    # 测试2: 修改所属公司
    print("\n===== 测试2: 修改所属公司 =====")
    # 先获取另一个公司ID，不同于原始公司ID
    other_company_id = get_other_company_id(original_company_id)
    if other_company_id:
        payload2 = {
            "id": grid_id,
            "companyId": other_company_id,
            "name": f"修改公司后的网格-测试-{grid_id}"
        }
        perform_test(url, headers, payload2)
    else:
        print("❌ 无法获取另一个公司ID进行测试，跳过该测试")
    
    # 测试3: 修改回原始公司
    print("\n===== 测试3: 修改回原始公司 =====")
    payload3 = {
        "id": grid_id,
        "companyId": original_company_id,
        "name": f"恢复原公司的网格-测试-{grid_id}"
    }
    perform_test(url, headers, payload3)
    
    # 测试4: 使用不存在的网格ID
    print("\n===== 测试4: 使用不存在的网格ID =====")
    payload4 = {
        "id": 99999,  # 假设这个ID不存在
        "name": "不存在的网格"
    }
    perform_test(url, headers, payload4)
    
    # 测试5: 使用不存在的公司ID
    print("\n===== 测试5: 使用不存在的公司ID =====")
    payload5 = {
        "id": grid_id,
        "companyId": 99999,  # 假设这个ID不存在
        "name": "测试不存在公司的网格"
    }
    perform_test(url, headers, payload5)

def perform_test(url, headers, payload):
    """执行测试并打印结果"""
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
                grid_data = data.get("data", {})
                print(f"\n✅ 测试成功: 网格修改成功")
                print(f"网格ID: {grid_data.get('id')}")
                print(f"网格名称: {grid_data.get('name')}")
                print(f"所属局点: {grid_data.get('companyName')} (ID: {grid_data.get('companyId')})")
                print(f"所属租户: {grid_data.get('tenantName')} (ID: {grid_data.get('tenantId')})")
                print(f"更新时间: {grid_data.get('updateTime')}")
            else:
                print(f"\n❌ 测试结果: {data.get('msg')}")
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")

def get_existing_grid():
    """获取一个现有网格用于测试"""
    try:
        url = "http://localhost:8080/ces/grid/list"
        payload = {"companyId": 0}  # 获取所有网格
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "00000" and data.get("data"):
                # 获取第一个网格
                grid = data.get("data")[0]
                
                # 获取更详细的网格信息，包括公司ID
                grid_detail = get_grid_detail(grid.get("id"))
                if grid_detail:
                    return grid_detail
                else:
                    print("无法获取网格详细信息")
                    return grid  # 返回基本信息
        
        print("无法获取现有网格")
        return None
    except Exception as e:
        print(f"获取网格时出错: {str(e)}")
        return None

def get_grid_detail(grid_id):
    """获取网格详细信息"""
    try:
        # 使用分页查询接口查询特定网格的详细信息
        url = "http://localhost:8080/ces/grid/list/page"
        payload = {"name": "", "pageNo": 1, "pageSize": 100, "companyId": 0}
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "00000" and data.get("data", {}).get("records"):
                records = data.get("data", {}).get("records", [])
                # 查找指定ID的网格
                for record in records:
                    if record.get("id") == grid_id:
                        return {
                            "id": record.get("id"),
                            "name": record.get("gridName"),
                            "companyId": record.get("companyId"),
                            "companyName": record.get("companyName"),
                            "tenantId": record.get("tenantId"),
                            "tenantName": record.get("tenantName")
                        }
        
        return None
    except Exception:
        return None

def get_other_company_id(current_company_id):
    """获取一个不同于当前公司ID的其他公司ID"""
    try:
        url = "http://localhost:8080/ces/company/list"
        payload = {"tenantId": 0}  # 获取所有公司
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "00000" and data.get("data"):
                companies = data.get("data")
                for company in companies:
                    if company.get("id") != current_company_id:
                        return company.get("id")
        
        return None
    except Exception:
        return None

if __name__ == "__main__":
    print("===== 测试网格修改接口 =====")
    test_grid_modify() 