import requests
import json

# 设置基础URL
BASE_URL = "http://localhost:8000"

def test_label_count_by_type(label_type=0):
    """测试标签总数量（按类型筛选）"""
    # 准备请求数据 - 查询标签
    data = {
        "name": "",
        "companyId": 0,
        "pageNo": 1,
        "pageSize": 100, # 设置较大的页面大小以获取所有标签
        "type": label_type
    }
    
    # 发送请求
    response = requests.post(f"{BASE_URL}/ces/label/list/page", json=data)
    
    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        return
    
    # 解析响应数据
    resp_data = response.json()
    
    if resp_data.get("code") != "00000":
        print(f"请求错误，错误代码: {resp_data.get('code')}, 错误信息: {resp_data.get('msg')}")
        return
    
    # 获取标签数量
    data = resp_data.get("data", {})
    total = data.get("total", 0)
    records = data.get("records", [])
    
    # 分类统计标签
    basic_labels = [label for label in records if label.get("type") == 1]
    advanced_labels = [label for label in records if label.get("type") == 2]
    
    # 输出结果
    type_desc = "全部" if label_type == 0 else ("基础" if label_type == 1 else "高级")
    print(f"========== {type_desc}标签数量统计 (type={label_type}) ==========")
    print(f"查询结果总数: {total}")
    print(f"基础标签数量: {len(basic_labels)}")
    print(f"高级标签数量: {len(advanced_labels)}")
    print("==================================")
    
    # 统计每个分类前5个标签
    if basic_labels:
        print(f"\n基础标签示例 (前5个):")
        for i, label in enumerate(basic_labels[:5]):
            company_names = label.get("companyNames", "")
            print(f"{i+1}. {label.get('name')} - 关联局点: {company_names}")
    
    if advanced_labels:
        print(f"\n高级标签示例 (前5个):")
        for i, label in enumerate(advanced_labels[:5]):
            company_names = label.get("companyNames", "")
            print(f"{i+1}. {label.get('name')} - 关联局点: {company_names}")

def main():
    """测试三种不同的type参数"""
    # 测试type=0（查询全部标签）
    test_label_count_by_type(0)
    print("\n")
    
    # 测试type=1（仅查询基础标签）
    test_label_count_by_type(1)
    print("\n")
    
    # 测试type=2（仅查询高级标签）
    test_label_count_by_type(2)

if __name__ == "__main__":
    main() 