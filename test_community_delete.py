import requests
import json

def test_community_delete(community_id):
    """测试删除小区接口"""
    url = f"http://localhost:8080/ces/community/delete?id={community_id}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # 发送DELETE请求
        response = requests.delete(url, headers=headers)
        
        # 打印状态码
        print(f"状态码: {response.status_code}")
        
        # 尝试解析JSON响应
        try:
            data = response.json()
            print(f"响应内容: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # 检查响应码
            if data.get("code") == "00000":
                community = data.get("data", {})
                
                print(f"\n✅ 测试成功: 小区删除成功")
                print(f"删除的小区ID: {community.get('id')}")
                print(f"小区名称: {community.get('name')}")
                print(f"所属网格: {community.get('gridName')} (ID: {community.get('gridId')})")
                print(f"所属局点: {community.get('companyName')} (ID: {community.get('companyId')})")
                print(f"所属运营商: {community.get('tenantName')} (ID: {community.get('tenantId')})")
                
                return True
            else:
                print(f"\n❌ 测试失败: {data.get('msg')}")
                return False
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        return False

def get_test_community_id():
    """获取一个测试用的小区ID"""
    print("\n===== 获取测试小区ID =====")
    
    # 使用分页查询接口获取小区列表
    url = "http://localhost:8080/ces/community/list/page"
    payload = {
        "pageNo": 1,
        "pageSize": 1
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "00000":
                records = data.get("data", {}).get("records", [])
                if records:
                    community_id = records[0].get("id")
                    print(f"获取到测试小区ID: {community_id}")
                    return community_id
                else:
                    print("未找到任何小区，请先添加小区")
                    return None
            else:
                print(f"查询失败: {data.get('msg')}")
                return None
        else:
            print(f"查询失败: 状态码 {response.status_code}")
            return None
    except Exception as e:
        print(f"查询失败: {str(e)}")
        return None

def create_test_community():
    """创建一个测试用的小区"""
    print("\n===== 创建测试小区 =====")
    
    # 先获取一个可用的网格ID
    url = "http://localhost:8080/ces/grid/list"
    payload = {
        "companyId": 0
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "00000":
                grids = data.get("data", [])
                if grids:
                    grid_id = grids[0].get("id")
                    
                    # 创建小区
                    create_url = "http://localhost:8080/ces/community/add"
                    create_payload = {
                        "gridId": grid_id,
                        "name": f"测试删除的小区-{grid_id}"
                    }
                    
                    create_response = requests.post(create_url, json=create_payload, headers=headers)
                    
                    if create_response.status_code == 200:
                        create_data = create_response.json()
                        if create_data.get("code") == "00000":
                            new_community_id = create_data.get("data", {}).get("id")
                            print(f"创建测试小区成功，ID: {new_community_id}")
                            return new_community_id
                        else:
                            print(f"创建小区失败: {create_data.get('msg')}")
                            return None
                    else:
                        print(f"创建小区请求失败，状态码: {create_response.status_code}")
                        return None
                else:
                    print("未找到任何网格，无法创建测试小区")
                    return None
            else:
                print(f"获取网格失败: {data.get('msg')}")
                return None
        else:
            print(f"获取网格请求失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"创建测试小区失败: {str(e)}")
        return None

def test_invalid_community_id():
    """测试删除不存在的小区"""
    print("\n===== 测试场景: 删除不存在的小区 =====")
    return test_community_delete(9999)

def verify_deletion(community_id):
    """验证小区是否被成功删除"""
    print(f"\n===== 验证小区ID {community_id} 是否被删除 =====")
    
    # 使用分页查询接口查找特定ID的小区
    url = "http://localhost:8080/ces/community/list/page"
    payload = {
        "pageNo": 1,
        "pageSize": 100
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "00000":
                records = data.get("data", {}).get("records", [])
                
                # 查找特定ID的小区
                for record in records:
                    if record.get("id") == community_id:
                        print(f"❌ 小区ID {community_id} 仍然存在，删除失败")
                        return False
                
                print(f"✅ 小区ID {community_id} 已成功删除")
                return True
            else:
                print(f"查询失败: {data.get('msg')}")
                return False
        else:
            print(f"查询失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"验证失败: {str(e)}")
        return False

if __name__ == "__main__":
    # 测试删除不存在的小区
    test_invalid_community_id()
    
    # 创建一个测试小区
    community_id = create_test_community()
    
    if community_id:
        # 测试删除小区
        print("\n===== 测试场景: 删除有效小区 =====")
        result = test_community_delete(community_id)
        
        if result:
            # 验证小区是否被成功删除
            verify_deletion(community_id)
    else:
        # 获取已有小区ID
        existing_community_id = get_test_community_id()
        
        if existing_community_id:
            # 测试删除小区
            print("\n===== 测试场景: 删除有效小区 =====")
            result = test_community_delete(existing_community_id)
            
            if result:
                # 验证小区是否被成功删除
                verify_deletion(existing_community_id)
        else:
            print("\n❌ 无法获取有效的小区ID，跳过删除测试") 