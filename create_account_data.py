import sqlite3
import datetime
import random
from models import engine, SessionLocal, UserAccount, Tenant, Company, Role, Group
from sqlalchemy.orm import Session
from sqlalchemy import text

def create_test_accounts():
    """
    创建测试账号数据
    """
    # 连接数据库会话
    db = SessionLocal()
    
    try:
        # 清空现有账号数据
        db.query(UserAccount).delete()
        db.commit()
        print("已清空现有账号数据")
        
        # 固定随机数种子，确保生成结果可重复
        random.seed(42)
        
        # 获取所有租户ID - 使用SQLAlchemy ORM查询
        tenants = db.query(Tenant).all()
        tenant_ids = [tenant.id for tenant in tenants]
        
        # 获取所有局点ID和租户ID - 使用SQLAlchemy ORM查询
        companies = db.query(Company).all()
        
        # 获取所有角色ID - 使用SQLAlchemy ORM查询
        roles = db.query(Role).all()
        role_ids = [role.id for role in roles] if roles else [1, 2, 3]  # 如果没有角色，使用默认值
        
        # 获取所有营销组ID - 使用SQLAlchemy ORM查询
        groups = db.query(Group).all()
        group_ids = [group.id for group in groups] if groups else [1, 2, 3]  # 如果没有营销组，使用默认值
        
        print(f"找到 {len(companies)} 个局点, {len(roles)} 个角色, {len(groups)} 个营销组")
        
        # 生成测试账号数据
        test_accounts = []
        
        # 普通账号模板
        account_templates = [
            {'prefix': 'admin', 'name_prefix': '管理员'},
            {'prefix': 'operator', 'name_prefix': '运营'},
            {'prefix': 'sales', 'name_prefix': '销售'},
            {'prefix': 'service', 'name_prefix': '客服'},
            {'prefix': 'tech', 'name_prefix': '技术'}
        ]
        
        # 为每个局点创建账号
        account_id = 1
        account_count = 0
        max_accounts = 30  # 最多创建30个账号
        
        for company in companies:
            # 如果已经达到最大账号数，退出循环
            if account_count >= max_accounts:
                break
                
            company_id = company.id
            tenant_id = company.tenant_id
            
            # 为每个账号模板创建账号
            for template in account_templates:
                # 如果已经达到最大账号数，退出循环
                if account_count >= max_accounts:
                    break
                    
                # 随机选择一个角色ID
                role_id = random.choice(role_ids) if role_ids else 1
                
                # 随机选择一个营销组ID
                group_id = random.choice(group_ids) if group_ids else None
                
                # 生成账号名
                account_name = f"{template['prefix']}_{company_id}"
                
                # 生成用户姓名
                real_name = f"{template['name_prefix']}{random.randint(1, 100)}"
                
                # 是否启用 (80%概率启用)
                is_enabled = 1 if random.random() < 0.8 else 0
                
                # 生成过期日期 (50%已过期, 50%未过期)
                expire_date = None
                if random.random() < 0.8:  # 80%的账号设置了过期日期
                    days = random.randint(-30, 180)  # 过期日期范围为30天前到180天后
                    expire_date = datetime.datetime.now() + datetime.timedelta(days=days)
                
                # 创建时间和更新时间
                create_time = datetime.datetime.now() - datetime.timedelta(
                    days=random.randint(30, 365))  # 创建时间为30-365天前
                update_time = create_time + datetime.timedelta(
                    days=random.randint(1, 30))  # 更新时间为创建后1-30天
                
                # 创建人
                creators = ["system", "admin", "supervisor"]
                creator = random.choice(creators)
                
                # 创建账号对象
                account = UserAccount(
                    id=account_id,
                    account=account_name,
                    name=real_name,
                    password="123456",  # 默认密码
                    tenant_id=tenant_id,
                    company_id=company_id,
                    role_id=role_id,
                    group_id=group_id,
                    is_enabled=is_enabled,
                    expire_date=expire_date,
                    create_time=create_time,
                    update_time=update_time,
                    creator=creator
                )
                
                test_accounts.append(account)
                account_id += 1
                account_count += 1
        
        # 将账号数据添加到数据库
        db.add_all(test_accounts)
        db.commit()
        
        print(f"成功创建了 {len(test_accounts)} 个测试账号")
        
        # 输出一些样本数据
        print("\n账号数据样例：")
        for account in test_accounts[:5]:
            expire_status = "未设置"
            if account.expire_date:
                if account.expire_date < datetime.datetime.now():
                    expire_status = "已过期"
                else:
                    expire_status = "未过期"
            
            enabled_status = "启用" if account.is_enabled == 1 else "禁用"
            
            print(f"ID: {account.id}, 账号: {account.account}, 姓名: {account.name}, "
                  f"角色ID: {account.role_id}, 状态: {enabled_status}, "
                  f"有效期: {account.expire_date}, {expire_status}")
            
    except Exception as e:
        db.rollback()
        print(f"创建测试账号数据时出错: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    # 初始化测试账号数据
    create_test_accounts() 