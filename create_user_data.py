import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random

# 创建数据库连接
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

def create_test_data():
    db = SessionLocal()
    try:
        # 获取所有租户
        tenants = db.query(models.Tenant).all()
        if not tenants:
            print("请先创建租户数据")
            return

        # 获取所有公司
        companies = db.query(models.Company).all()
        if not companies:
            print("请先创建公司数据")
            return

        # 获取所有班组
        groups = db.query(models.Group).all()
        if not groups:
            print("请先创建班组数据")
            return

        # 获取所有角色
        roles = db.query(models.Role).all()
        if not roles:
            print("请先创建角色数据")
            return

        # 生成30个用户
        for i in range(30):
            # 随机选择租户和公司
            tenant = random.choice(tenants)
            company = random.choice(companies)
            
            # 生成用户名和姓名
            username = f"user{i+1}"
            name = f"用户{i+1}"
            
            # 生成有效期（1-365天）
            days = random.randint(1, 365)
            effective_day = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
            
            # 创建用户
            user = models.User(
                username=username,
                name=name,
                tenant_id=tenant.id,
                company_id=company.id,
                effective_day=effective_day,
                status=random.choice([0, 1]),  # 随机状态
                expire=random.choice([1, 2]),  # 随机是否到期
                create_time=datetime.now(),
                update_time=datetime.now(),
                operator_name="admin"
            )
            
            # 随机分配1-3个班组
            user_groups = random.sample(groups, random.randint(1, 3))
            user.groups = user_groups
            
            # 随机分配1-2个角色
            user_roles = random.sample(roles, random.randint(1, 2))
            user.roles = user_roles
            
            db.add(user)
        
        db.commit()
        print("成功创建30个用户数据")
        
    except Exception as e:
        db.rollback()
        print(f"创建数据失败: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data() 