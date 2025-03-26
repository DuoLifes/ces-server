import requests
import json

def test_community_list_page(company_id=0, grid_id=0, community_name="", page_no=1, page_size=10, tenant_id=0):
    """测试小区分页查询接口"""
    url = "http://localhost:8080/ces/community/list/page"
    payload = {
        "companyId": company_id,
        "gridId": grid_id,
        "name": community_name,
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
            
            # 检查响应码
            if data.get("code") == "00000":
                records = data.get("data", {}).get("records", [])
                total = data.get("data", {}).get("total", 0)
                current = data.get("data", {}).get("current", 0)
                size = data.get("data", {}).get("size", 0)
                pages = data.get("data", {}).get("pages", 0)
                
                print(f"\n✅ 测试成功: 获取到 {len(records)} 条记录")
                print(f"总记录数: {total}, 当前页: {current}, 每页大小: {size}, 总页数: {pages}")
                
                # 打印前10条记录
                if records:
                    print("\n小区列表(前10条):")
                    for i, record in enumerate(records[:10], 1):
                        print(f"{i}. ID: {record.get('id')}, 名称: {record.get('name')}")
                        print(f"   所属网格: {record.get('gridName')} (ID: {record.get('gridId')})")
                        print(f"   所属局点: {record.get('companyName')} (ID: {record.get('companyId')})")
                        print(f"   所属运营商: {record.get('tenantName')} (ID: {record.get('tenantId')})")
                        print(f"   创建时间: {record.get('createTime')}, 更新时间: {record.get('updateTime')}")
                        print(f"   操作人: {record.get('operatorName')}")
                    
                    if len(records) > 10:
                        print(f"... 还有 {len(records) - 10} 条记录未显示")
            else:
                print(f"\n❌ 测试失败: {data.get('msg')}")
        except json.JSONDecodeError:
            print("\n❌ 测试失败: 响应不是有效的JSON格式")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")

if __name__ == "__main__":
    # 测试场景1: 查询所有小区
    print("===== 测试场景1: 查询所有小区 =====")
    test_community_list_page()
    
    # 测试场景2: 按公司ID筛选
    print("\n===== 测试场景2: 按公司ID筛选 =====")
    test_community_list_page(company_id=2)
    
    # 测试场景3: 按网格ID筛选
    print("\n===== 测试场景3: 按网格ID筛选 =====")
    test_community_list_page(grid_id=5)
    
    # 测试场景4: 按租户ID筛选
    print("\n===== 测试场景4: 按租户ID筛选 =====")
    test_community_list_page(tenant_id=1)
    
    # 测试场景5: 名称模糊查询
    print("\n===== 测试场景5: 名称模糊查询 =====")
    test_community_list_page(community_name="和平")
    
    # 测试场景6: 组合条件查询
    print("\n===== 测试场景6: 组合条件查询 =====")
    test_community_list_page(company_id=3, community_name="花园")
    
    # 测试场景7: 分页测试 - 第1页，每页5条
    print("\n===== 测试场景7: 分页测试 - 第1页，每页5条 =====")
    test_community_list_page(page_no=1, page_size=5)
    
    # 测试场景8: 分页测试 - 第2页，每页5条
    print("\n===== 测试场景8: 分页测试 - 第2页，每页5条 =====")
    test_community_list_page(page_no=2, page_size=5) 