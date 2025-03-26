from models import SessionLocal, Group, Company
import random
import datetime

# 创建数据库会话
db = SessionLocal()

try:
    # 获取所有公司记录
    companies = db.query(Company).all()
    
    if not companies:
        print("错误：数据库中没有公司记录。请先添加公司数据。")
        exit(1)
    
    # 营销组名称前缀列表
    group_name_prefixes = [
        "销售", "市场", "客户", "运营", "直销", "渠道", "方案", "行业", "企业", "小微"
    ]
    
    # 营销组名称后缀列表
    group_name_suffixes = [
        "一组", "二组", "三组", "团队", "中心", "小组", "部门", "事业部", "营销组", "服务组"
    ]
    
    # 营销组描述列表
    descriptions = [
        "负责社区销售和客户维护",
        "主要开展市场推广活动",
        "专注企业客户服务",
        "负责新用户开发",
        "处理客户投诉和维系",
        "针对校园市场开展业务",
        "专注商业区域拓展",
        "负责产品销售和推广",
        "主要做用户留存和价值提升",
        "负责新技术应用推广",
        None  # 有些描述可以为空
    ]
    
    # 操作员名称列表
    operators = ["管理员", "系统管理员", "超级管理员", "运维人员", "数据管理员"]
    
    # 生成30个营销组数据
    for i in range(1, 31):
        # 随机选择一个公司
        company = random.choice(companies)
        
        # 随机生成营销组名称
        name = random.choice(group_name_prefixes) + random.choice(group_name_suffixes)
        
        # 随机选择描述，有10%概率为空
        description = random.choice(descriptions)
        
        # 随机生成创建和更新时间（过去90天内）
        days_ago = random.randint(1, 90)
        create_time = datetime.datetime.now() - datetime.timedelta(days=days_ago)
        update_time = create_time + datetime.timedelta(days=random.randint(0, days_ago))
        
        # 随机选择操作员
        operator_name = random.choice(operators)
        
        # 创建营销组对象
        group = Group(
            name=name,
            description=description,
            company_id=company.id,
            create_time=create_time,
            update_time=update_time,
            operator_name=operator_name
        )
        
        # 添加到数据库会话
        db.add(group)
        
    # 提交事务
    db.commit()
    print(f"成功添加了30条营销组数据")

except Exception as e:
    # 发生错误时回滚事务
    db.rollback()
    print(f"添加营销组数据时发生错误: {e}")

finally:
    # 关闭数据库会话
    db.close() 