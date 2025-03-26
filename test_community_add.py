import requests
import json

def test_community_add(grid_id, name):
    """测试新增小区接口"""
    url = "http://localhost:8080/ces/community/add"
    payload = {
        "gridId": grid_id,
        "name": name
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
                community = data.get("data", {})
                
                print(f"\n✅ 测试成功: 小区添加成功")
                print(f"小区ID: {community.get('id')}")
                print(f"小区名称: {community.get('name')}")
                print(f"所属网格: {community.get('gridName')} (ID: {community.get('gridId')})")
                print(f"所属局点: {community.get('companyName')} (ID: {community.get('companyId')})")
                print(f"所属运营商: {community.get('tenantName')} (ID: {community.get('tenantId')})")
                print(f"创建时间: {community.get('createTime')}")
                print(f"更新时间: {community.get('updateTime')}")
                print(f"操作人: {community.get('operatorName')}")
                
                return community.get('id')  # 返回新创建的小区ID
            else:
                print(f"\n❌ 测试失败: {data.get('msg')}")
                return None
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
            return None
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        return None

def test_invalid_grid_id():
    """测试无效的网格ID"""
    print("\n===== 测试场景: 无效的网格ID =====")
    return test_community_add(9999, "测试小区")

def test_empty_name():
    """测试空名称"""
    print("\n===== 测试场景: 空名称 =====")
    return test_community_add(1, "")

def test_valid_community():
    """测试有效的小区添加"""
    print("\n===== 测试场景: 有效的小区添加 =====")
    return test_community_add(1, "测试新增小区")

def test_query_by_id(community_id):
    """测试查询新增的小区"""
    if not community_id:
        print("\n跳过查询测试: 未获取到有效的小区ID")
        return
        
    print(f"\n===== 测试场景: 查询新增的小区 (ID: {community_id}) =====")
    
    # 使用分页查询接口查询特定小区
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
                
                # 查找指定ID的小区
                for record in records:
                    if record.get("id") == community_id:
                        print(f"\n✅ 成功查询到新增小区:")
                        print(f"小区ID: {record.get('id')}")
                        print(f"小区名称: {record.get('name')}")
                        print(f"所属网格: {record.get('gridName')} (ID: {record.get('gridId')})")
                        print(f"所属局点: {record.get('companyName')} (ID: {record.get('companyId')})")
                        print(f"所属运营商: {record.get('tenantName')} (ID: {record.get('tenantId')})")
                        return
                
                print(f"\n❌ 未找到ID为 {community_id} 的小区")
            else:
                print(f"\n❌ 查询失败: {data.get('msg')}")
        else:
            print(f"\n❌ 查询失败: 状态码 {response.status_code}")
    except Exception as e:
        print(f"\n❌ 查询失败: {str(e)}")

if __name__ == "__main__":
    # 测试无效的网格ID
    test_invalid_grid_id()
    
    # 测试空名称
    test_empty_name()
    
    # 测试有效的小区添加
    community_id = test_valid_community()
    
    # 测试查询新增的小区
    test_query_by_id(community_id) 