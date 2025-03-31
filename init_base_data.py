import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 创建数据库连接
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

def create_base_data():
    db = SessionLocal()
    try:
        # 创建租户
        tenants = [
            models.Tenant(name="租户1"),
            models.Tenant(name="租户2"),
            models.Tenant(name="租户3")
        ]
        db.add_all(tenants)
        db.commit()

        # 为每个租户创建公司
        companies = []
        for tenant in tenants:
            for i in range(2):
                company = models.Company(
                    name=f"{tenant.name}-公司{i+1}",
                    tenant_id=tenant.id
                )
                companies.append(company)
        db.add_all(companies)
        db.commit()

        # 为每个公司创建班组
        groups = []
        for company in companies:
            for i in range(2):
                group = models.Group(
                    name=f"{company.name}-班组{i+1}",
                    description=f"{company.name}的班组{i+1}",
                    company_id=company.id,
                    create_time=datetime.now(),
                    update_time=datetime.now(),
                    operator_name="admin"
                )
                groups.append(group)
        db.add_all(groups)
        db.commit()

        # 创建角色
        roles = [
            models.Role(
                name="管理员",
                description="系统管理员",
                create_time=datetime.now(),
                update_time=datetime.now(),
                operator_name="admin"
            ),
            models.Role(
                name="普通用户",
                description="普通用户",
                create_time=datetime.now(),
                update_time=datetime.now(),
                operator_name="admin"
            )
        ]
        db.add_all(roles)
        db.commit()

        print("成功创建基础数据")
        
    except Exception as e:
        db.rollback()
        print(f"创建数据失败: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_base_data() 