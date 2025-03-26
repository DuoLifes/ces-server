import requests
import json

def test_community_modify(community_id, grid_id=None, name=None):
    """测试修改小区接口"""
    url = "http://localhost:8080/ces/community/modify"
    
    # 构建请求参数，仅包含非None的参数
    payload = {"id": community_id}
    if grid_id is not None:
        payload["gridId"] = grid_id
    if name is not None:
        payload["name"] = name
    
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
                community = data.get("data", {})
                
                print(f"\n✅ 测试成功: 小区修改成功")
                print(f"小区ID: {community.get('id')}")
                print(f"小区名称: {community.get('name')}")
                print(f"所属网格: {community.get('gridName')} (ID: {community.get('gridId')})")
                print(f"所属局点: {community.get('companyName')} (ID: {community.get('companyId')})")
                print(f"所属运营商: {community.get('tenantName')} (ID: {community.get('tenantId')})")
                print(f"创建时间: {community.get('createTime')}")
                print(f"更新时间: {community.get('updateTime')}")
                print(f"操作人: {community.get('operatorName')}")
                
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
                    return community_id, records[0]
                else:
                    print("未找到任何小区，请先添加小区")
                    return None, None
            else:
                print(f"查询失败: {data.get('msg')}")
                return None, None
        else:
            print(f"查询失败: 状态码 {response.status_code}")
            return None, None
    except Exception as e:
        print(f"查询失败: {str(e)}")
        return None, None

def get_test_grid_id(current_grid_id=None):
    """获取一个与当前不同的测试用的网格ID"""
    print("\n===== 获取测试网格ID =====")
    
    # 使用网格列表接口获取网格
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
                    # 查找一个与当前不同的网格ID
                    for grid in grids:
                        grid_id = grid.get("id")
                        if grid_id != current_grid_id:
                            print(f"获取到测试网格ID: {grid_id}，名称: {grid.get('name')}")
                            return grid_id
                    # 所有网格都与当前网格相同，直接返回第一个
                    grid_id = grids[0].get("id")
                    print(f"未找到不同的网格，使用相同网格ID: {grid_id}")
                    return grid_id
                else:
                    print("未找到任何网格，请先添加网格")
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

def test_invalid_community_id():
    """测试无效的小区ID"""
    print("\n===== 测试场景: 无效的小区ID =====")
    return test_community_modify(9999, name="测试修改小区名称")

def test_invalid_grid_id(community_id):
    """测试无效的网格ID"""
    print("\n===== 测试场景: 无效的网格ID =====")
    return test_community_modify(community_id, grid_id=9999)

def test_empty_name(community_id):
    """测试空名称"""
    print("\n===== 测试场景: 空名称 =====")
    return test_community_modify(community_id, name="")

def test_modify_name(community_id):
    """测试修改小区名称"""
    print("\n===== 测试场景: 修改小区名称 =====")
    return test_community_modify(community_id, name="修改后的小区名称")

def test_modify_grid(community_id, new_grid_id):
    """测试修改小区网格"""
    print("\n===== 测试场景: 修改小区网格 =====")
    return test_community_modify(community_id, grid_id=new_grid_id)

def test_modify_both(community_id, new_grid_id):
    """测试同时修改小区名称和网格"""
    print("\n===== 测试场景: 同时修改小区名称和网格 =====")
    return test_community_modify(community_id, grid_id=new_grid_id, name="同时修改名称和网格")

if __name__ == "__main__":
    # 获取测试小区ID
    community_id, community_info = get_test_community_id()
    
    # 获取测试网格ID
    if community_id and community_info:
        current_grid_id = community_info.get("gridId")
        new_grid_id = get_test_grid_id(current_grid_id)
        
        # 测试无效的小区ID
        test_invalid_community_id()
        
        if new_grid_id:
            # 测试无效的网格ID
            test_invalid_grid_id(community_id)
            
            # 测试空名称
            test_empty_name(community_id)
            
            # 测试修改小区名称
            test_modify_name(community_id)
            
            # 测试修改小区网格
            test_modify_grid(community_id, new_grid_id)
            
            # 测试同时修改小区名称和网格
            test_modify_both(community_id, new_grid_id)
        else:
            print("\n❌ 无法获取测试网格ID，跳过网格相关测试")
    else:
        print("\n❌ 无法获取测试小区ID，跳过测试") 