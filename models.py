from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    # 与Company的关系
    companies = relationship("Company", back_populates="tenant")

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    
    # 与Tenant的关系
    tenant = relationship("Tenant", back_populates="companies")
    # 与Grid的关系
    grids = relationship("Grid", back_populates="company")

class Grid(Base):
    __tablename__ = "grids"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    
    # 与Company的关系
    company = relationship("Company", back_populates="grids")
    # 与Community的关系
    communities = relationship("Community", back_populates="grid")

class Community(Base):
    __tablename__ = "communities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    grid_id = Column(Integer, ForeignKey("grids.id"))
    create_time = Column(DateTime, default=datetime.datetime.now)
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    operator_name = Column(String, default="管理员")
    
    # 与Grid的关系
    grid = relationship("Grid", back_populates="communities")

class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)                    # 营销组名称
    description = Column(String, nullable=True)         # 营销组描述
    company_id = Column(Integer, ForeignKey("companies.id"))   # 所属局点ID
    create_time = Column(DateTime, default=datetime.datetime.now)
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    operator_name = Column(String, default="管理员")
    
    # 与Company的关系
    company = relationship("Company")

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)                    # 角色名称
    description = Column(String, nullable=True)          # 角色描述
    create_time = Column(DateTime, default=datetime.datetime.now)
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    operator_name = Column(String, default="管理员")

class Label(Base):
    __tablename__ = "labels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)                    # 标签名称
    type = Column(Integer)                               # 标签类别（1:基础标签，2:高级标签）
    create_time = Column(DateTime, default=datetime.datetime.now)
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    operator_name = Column(String, default="管理员")
    
    # 与LabelCompany的关系
    companies = relationship("LabelCompany", back_populates="label")

class LabelCompany(Base):
    __tablename__ = "label_companies"
    
    id = Column(Integer, primary_key=True, index=True)
    label_id = Column(Integer, ForeignKey("labels.id"))      # 标签ID
    company_id = Column(Integer, ForeignKey("companies.id")) # 局点ID
    
    # 与Label的关系
    label = relationship("Label", back_populates="companies")
    # 与Company的关系
    company = relationship("Company")

# 账号模型 - 扩展User模型，增加更多业务字段
class UserAccount(Base):
    __tablename__ = "user_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    account = Column(String, unique=True, index=True)  # 用户账号
    name = Column(String, index=True)                  # 用户名称
    password = Column(String)                          # 密码
    tenant_id = Column(Integer, ForeignKey("tenants.id"))  # 运营商ID
    company_id = Column(Integer, ForeignKey("companies.id"))  # 局点ID
    group_id = Column(Integer, ForeignKey("groups.id"))  # 单一营销组ID (保留兼容性)
    role_id = Column(Integer, ForeignKey("roles.id"))  # 角色ID
    is_enabled = Column(Integer, default=1)  # 是否启用 1:启用, 0:禁用
    expire_date = Column(DateTime, nullable=True)  # 有效期至
    create_time = Column(DateTime, default=datetime.datetime.now)  # 创建时间
    update_time = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 更新时间
    creator = Column(String, default="管理员")  # 创建人
    
    # 关系
    tenant = relationship("Tenant")
    company = relationship("Company")
    group = relationship("Group")
    role = relationship("Role")
    # 与AccountGroup的关系
    groups = relationship("AccountGroup", back_populates="account")

# 账号与营销组的关联表
class AccountGroup(Base):
    __tablename__ = "account_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("user_accounts.id"))  # 账号ID
    group_id = Column(Integer, ForeignKey("groups.id"))  # 营销组ID
    
    # 与UserAccount的关系
    account = relationship("UserAccount", back_populates="groups")
    # 与Group的关系
    group = relationship("Group")

# 确保更新数据库表结构
print("正在更新数据库表结构...")
Base.metadata.create_all(bind=engine) 