from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
import random
import datetime

# 连接数据库
engine = create_engine("sqlite:///./sql_app.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# 角色列表
role_list = [
    {"name": "系统管理员", "description": "负责系统全局配置和用户管理"},
    {"name": "运营主管", "description": "负责整体运营策略和方向"},
    {"name": "销售经理", "description": "负责销售团队管理和销售策略"},
    {"name": "销售专员", "description": "负责具体销售工作"},
    {"name": "市场经理", "description": "负责市场策略和营销活动"},
    {"name": "市场专员", "description": "负责具体市场活动执行"},
    {"name": "客服主管", "description": "负责客服团队管理"},
    {"name": "客服专员", "description": "负责处理客户咨询和投诉"},
    {"name": "财务主管", "description": "负责财务预算和资金管理"},
    {"name": "财务专员", "description": "负责日常财务记录和报表"},
    {"name": "人力资源主管", "description": "负责人才招聘和团队建设"},
    {"name": "人力资源专员", "description": "负责员工入职和档案管理"},
    {"name": "技术主管", "description": "负责技术团队管理和技术方向"},
    {"name": "开发工程师", "description": "负责系统功能开发"},
    {"name": "测试工程师", "description": "负责系统功能测试"},
    {"name": "运维工程师", "description": "负责系统维护和稳定性"},
    {"name": "产品经理", "description": "负责产品规划和功能设计"},
    {"name": "产品专员", "description": "负责产品文档和用户反馈"},
    {"name": "数据分析师", "description": "负责数据分析和报表生成"},
    {"name": "培训讲师", "description": "负责员工培训和能力提升"}
]

def create_roles():
    # 先删除现有角色数据
    try:
        existing_roles = db.query(models.Role).all()
        for role in existing_roles:
            db.delete(role)
        db.commit()
        print(f"已删除 {len(existing_roles)} 条现有角色数据")
    except Exception as e:
        db.rollback()
        print(f"删除现有角色数据失败: {str(e)}")
    
    # 插入新角色数据
    inserted_count = 0
    for role_data in role_list:
        try:
            # 创建新角色
            new_role = models.Role(
                name=role_data["name"],
                description=role_data["description"],
                create_time=datetime.datetime.now(),
                update_time=datetime.datetime.now(),
                operator_name="数据初始化脚本"
            )
            
            # 添加到数据库
            db.add(new_role)
            db.commit()
            
            print(f"已创建角色: {role_data['name']}")
            inserted_count += 1
        except Exception as e:
            db.rollback()
            print(f"创建角色 {role_data['name']} 失败: {str(e)}")
    
    print(f"成功插入 {inserted_count} 条角色数据")

if __name__ == "__main__":
    create_roles() 