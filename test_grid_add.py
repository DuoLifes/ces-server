import requests
import json

def test_grid_add():
    """测试网格新增接口"""
    url = "http://localhost:8080/ces/grid/add"
    headers = {
        "Content-Type": "application/json"
    }
    
    # 测试数据
    payload = {
        "companyId": 1,  # 联通-北京分公司
        "name": "测试新增网格-联通北京专属网格"
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
                grid_data = data.get("data", {})
                print(f"\n✅ 测试成功: 网格添加成功")
                print(f"网格ID: {grid_data.get('id')}")
                print(f"网格名称: {grid_data.get('name')}")
                print(f"所属局点: {grid_data.get('companyName')} (ID: {grid_data.get('companyId')})")
                print(f"所属租户: {grid_data.get('tenantName')} (ID: {grid_data.get('tenantId')})")
                print(f"创建时间: {grid_data.get('createTime')}")
            else:
                print(f"\n❌ 测试失败: {data.get('msg')}")
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    print("===== 测试网格新增接口 =====")
    test_grid_add() 