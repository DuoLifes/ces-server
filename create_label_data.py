from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
import random
import datetime

# 连接数据库
engine = create_engine("sqlite:///./sql_app.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# 基础标签列表 (25条)
basic_labels = [
    "忠诚客户",
    "高价值客户",
    "流失风险客户",
    "新注册客户",
    "5G套餐客户",
    "商务客户",
    "家庭宽带客户",
    "校园客户",
    "老年客户",
    "异地客户",
    "4G客户",
    "3G客户",
    "国际漫游客户",
    "港澳台漫游客户",
    "预付费客户",
    "后付费客户",
    "话费欠费客户",
    "话费风险客户",
    "终端老旧客户",
    "政企客户",
    "小微企业客户",
    "个体户客户",
    "低消费客户",
    "中等消费客户",
    "高消费客户"
]

# 高级标签列表 (25条)
advanced_labels = [
    "高流量客户",
    "低流量客户",
    "异网携入客户",
    "多卡用户",
    "游戏用户",
    "视频用户",
    "跨域漫游用户",
    "套餐升级意向客户",
    "套餐降级意向客户",
    "增值业务意向客户",
    "频繁投诉客户",
    "满意度低客户",
    "满意度高客户",
    "夜间活跃客户",
    "白天活跃客户",
    "周末活跃客户",
    "工作日活跃客户",
    "社交APP用户",
    "购物APP用户",
    "金融APP用户",
    "教育APP用户",
    "医疗APP用户",
    "出行APP用户",
    "音乐APP用户",
    "阅读APP用户"
]

def create_labels():
    # 先删除现有标签数据
    try:
        # 删除标签与局点的关联
        db.query(models.LabelCompany).delete()
        db.commit()
        
        # 删除标签
        existing_labels = db.query(models.Label).all()
        for label in existing_labels:
            db.delete(label)
        db.commit()
        print(f"已删除 {len(existing_labels)} 条现有标签数据")
    except Exception as e:
        db.rollback()
        print(f"删除现有标签数据失败: {str(e)}")
    
    # 插入基础标签数据
    inserted_count = 0
    for label_name in basic_labels:
        try:
            # 创建基础标签
            new_label = models.Label(
                name=label_name,
                type=1,  # 基础标签
                create_time=datetime.datetime.now(),
                update_time=datetime.datetime.now(),
                operator_name="数据初始化脚本"
            )
            
            # 添加到数据库
            db.add(new_label)
            db.commit()
            db.refresh(new_label)
            
            # 随机关联1-3个局点
            companies = db.query(models.Company).all()
            if companies:
                sample_count = min(3, len(companies))
                selected_companies = random.sample(companies, sample_count)
                
                for company in selected_companies:
                    label_company = models.LabelCompany(
                        label_id=new_label.id,
                        company_id=company.id
                    )
                    db.add(label_company)
                
                db.commit()
            
            print(f"已创建基础标签: {label_name}")
            inserted_count += 1
        except Exception as e:
            db.rollback()
            print(f"创建基础标签 {label_name} 失败: {str(e)}")
    
    # 插入高级标签数据
    for label_name in advanced_labels:
        try:
            # 创建高级标签
            new_label = models.Label(
                name=label_name,
                type=2,  # 高级标签
                create_time=datetime.datetime.now(),
                update_time=datetime.datetime.now(),
                operator_name="数据初始化脚本"
            )
            
            # 添加到数据库
            db.add(new_label)
            db.commit()
            db.refresh(new_label)
            
            # 随机关联1-3个局点
            companies = db.query(models.Company).all()
            if companies:
                sample_count = min(3, len(companies))
                selected_companies = random.sample(companies, sample_count)
                
                for company in selected_companies:
                    label_company = models.LabelCompany(
                        label_id=new_label.id,
                        company_id=company.id
                    )
                    db.add(label_company)
                
                db.commit()
            
            print(f"已创建高级标签: {label_name}")
            inserted_count += 1
        except Exception as e:
            db.rollback()
            print(f"创建高级标签 {label_name} 失败: {str(e)}")
    
    print(f"成功插入 {inserted_count} 条标签数据")

if __name__ == "__main__":
    create_labels() 