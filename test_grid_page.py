import requests
import json

def test_grid_list_page(company_id=0, grid_name="", page_no=1, page_size=10, tenant_id=0):
    """测试网格分页查询接口"""
    url = "http://localhost:8080/ces/grid/list/page"
    payload = {
        "companyId": company_id,
        "name": grid_name,
        "pageNo": page_no,
        "pageSize": page_size,
        "tenantId": tenant_id
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
            
            # 如果成功获取数据，打印更多详细信息
            if data.get("code") == "00000":
                page_data = data.get("data", {})
                records = page_data.get("records", [])
                
                print(f"\n✅ 测试成功")
                print(f"总记录数: {page_data.get('total')}")
                print(f"当前页: {page_data.get('current')}")
                print(f"每页大小: {page_data.get('size')}")
                print(f"总页数: {page_data.get('pages')}")
                
                # 打印网格详情
                if records:
                    print("\n网格详情:")
                    for i, record in enumerate(records, 1):
                        print(f"{i}. ID: {record.get('id')}, " +
                              f"网格: {record.get('gridName')}, " +
                              f"所属公司: {record.get('companyName')} (ID: {record.get('companyId')}), " +
                              f"所属租户: {record.get('tenantName')} (ID: {record.get('tenantId')})")
                else:
                    print("\n没有符合条件的网格")
            else:
                print(f"\n❌ 测试失败: {data.get('msg')}")
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    # 测试场景1: 查询所有网格
    print("===== 测试场景1: 查询所有网格 =====")
    test_grid_list_page()
    
    # 测试场景2: 按公司ID筛选
    print("\n===== 测试场景2: 按公司ID筛选 =====")
    test_grid_list_page(company_id=2)
    
    # 测试场景3: 按租户ID筛选
    print("\n===== 测试场景3: 按租户ID筛选 =====")
    test_grid_list_page(tenant_id=1)
    
    # 测试场景4: 名称模糊查询
    print("\n===== 测试场景4: 名称模糊查询 =====")
    test_grid_list_page(grid_name="网格1")
    
    # 测试场景5: 组合条件查询
    print("\n===== 测试场景5: 组合条件查询 =====")
    test_grid_list_page(company_id=3, grid_name="移动")
    
    # 测试场景6: 分页测试 - 第1页，每页2条
    print("\n===== 测试场景6: 分页测试 - 第1页，每页2条 =====")
    test_grid_list_page(page_no=1, page_size=2)
    
    # 测试场景7: 分页测试 - 第2页，每页2条
    print("\n===== 测试场景7: 分页测试 - 第2页，每页2条 =====")
    test_grid_list_page(page_no=2, page_size=2) 