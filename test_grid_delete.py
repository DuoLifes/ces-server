import requests
import json

def test_grid_delete():
    """测试网格删除接口"""
    # 步骤1: 先获取一个可用的网格ID，为了测试不影响现有网格，我们先创建一个新网格
    grid_id = create_test_grid()
    if not grid_id:
        print("❌ 无法创建测试网格，测试终止")
        return
    
    print(f"\n===== 测试删除网格 (ID: {grid_id}) =====")
    
    # 步骤2: 调用删除接口
    url = f"http://localhost:8080/ces/grid/delete?id={grid_id}"
    
    try:
        # 发送DELETE请求
        response = requests.delete(url)
        
        # 打印状态码
        print(f"状态码: {response.status_code}")
        
        # 尝试解析JSON响应
        try:
            data = response.json()
            print(f"响应内容: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # 检查响应码
            if data.get("code") == "00000":
                grid_data = data.get("data", {})
                print(f"\n✅ 测试成功: 网格删除成功")
                print(f"网格ID: {grid_data.get('id')}")
                print(f"网格名称: {grid_data.get('name')}")
                print(f"所属局点: {grid_data.get('companyName')} (ID: {grid_data.get('companyId')})")
                print(f"所属租户: {grid_data.get('tenantName')} (ID: {grid_data.get('tenantId')})")
                
                # 步骤3: 确认网格已被删除
                confirm_deletion(grid_id)
            else:
                print(f"\n❌ 测试失败: {data.get('msg')}")
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
    
    # 测试删除不存在的网格
    print("\n===== 测试删除不存在的网格 =====")
    test_non_existent_grid()

def create_test_grid():
    """创建一个测试网格用于删除测试"""
    url = "http://localhost:8080/ces/grid/add"
    headers = {"Content-Type": "application/json"}
    
    # 获取一个可用的公司ID
    company_id = get_available_company_id()
    if not company_id:
        print("无法获取可用的公司ID")
        return None
    
    # 创建测试网格
    payload = {
        "companyId": company_id,
        "name": f"测试删除用网格-{company_id}-{get_timestamp()}"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "00000" and data.get("data"):
                grid_id = data.get("data").get("id")
                print(f"已创建测试网格，ID: {grid_id}，用于删除测试")
                return grid_id
    except Exception as e:
        print(f"创建测试网格失败: {str(e)}")
    
    return None

def get_available_company_id():
    """获取一个可用的公司ID"""
    try:
        url = "http://localhost:8080/ces/company/list"
        response = requests.post(url, json={"tenantId": 0}, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "00000" and data.get("data"):
                # 返回第一个公司的ID
                return data.get("data")[0].get("id")
    except Exception:
        pass
    
    return None

def confirm_deletion(grid_id):
    """确认网格已被删除"""
    try:
        url = "http://localhost:8080/ces/grid/list/page"
        payload = {"name": "", "pageNo": 1, "pageSize": 1000, "companyId": 0}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "00000" and data.get("data", {}).get("records"):
                records = data.get("data", {}).get("records", [])
                
                # 查找是否还存在此ID的网格
                for record in records:
                    if record.get("id") == grid_id:
                        print(f"\n❌ 验证失败: 网格ID {grid_id} 仍然存在于数据库中")
                        return
                
                print(f"\n✅ 验证成功: 网格ID {grid_id} 已从数据库中删除")
                return
            
        print("\n❓ 无法验证网格是否已删除")
    except Exception as e:
        print(f"\n❓ 验证网格删除时出错: {str(e)}")

def test_non_existent_grid():
    """测试删除不存在的网格ID"""
    grid_id = 99999  # 假设这个ID不存在
    url = f"http://localhost:8080/ces/grid/delete?id={grid_id}"
    
    try:
        response = requests.delete(url)
        print(f"状态码: {response.status_code}")
        
        try:
            data = response.json()
            print(f"响应内容: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            if data.get("code") == "A0001" and "不存在" in data.get("msg", ""):
                print(f"\n✅ 测试成功: 系统正确识别出网格ID {grid_id} 不存在")
            else:
                print(f"\n❌ 测试意外: 删除不存在的网格返回了意外的响应")
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")

def get_timestamp():
    """获取当前时间戳，用于创建唯一名称"""
    import time
    return int(time.time())

if __name__ == "__main__":
    print("===== 测试网格删除接口 =====")
    test_grid_delete() 