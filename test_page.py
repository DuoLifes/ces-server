import requests
import json

def test_company_list_page():
    """测试公司分页查询接口"""
    url = "http://localhost:8080/ces/company/list/page"
    payload = {
        "companyName": "",
        "pageNo": 1,
        "pageSize": 10,
        "tenantId": 0
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
                
                print(f"\n总记录数: {page_data.get('total')}")
                print(f"当前页: {page_data.get('current')}")
                print(f"每页大小: {page_data.get('size')}")
                print(f"总页数: {page_data.get('pages')}")
                
                # 打印记录详情
                if records:
                    print("\n记录详情:")
                    for i, record in enumerate(records, 1):
                        print(f"{i}. ID: {record.get('id')}, 名称: {record.get('name')}, 租户ID: {record.get('tenantId')}")
                else:
                    print("\n没有记录")
            else:
                print(f"\n请求失败: {data.get('msg')}")
                
        except json.JSONDecodeError:
            print("响应不是有效的JSON格式")
            print(f"原始响应: {response.text}")
    
    except requests.RequestException as e:
        print(f"请求失败: {str(e)}")

if __name__ == "__main__":
    test_company_list_page() 