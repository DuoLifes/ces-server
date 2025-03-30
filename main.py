from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import PlainTextResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import models
import utils
from pydantic import BaseModel, Field
import jwt
from typing import Optional, List, Union, Any, Dict
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_
import math
import random

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

@app.get("/")
async def root():
    return PlainTextResponse("Server is Running")

# 依赖项
def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic模型
class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class CommonResponse(BaseModel):
    code: str
    msg: str
    data: Optional[str] = None

class TenantItem(BaseModel):
    id: int
    name: str

class TenantListResponse(BaseModel):
    code: str
    msg: str
    data: List[TenantItem]

# 定义公司模型
class CompanyItem(BaseModel):
    id: int
    name: str

# 公司列表响应模型
class CompanyListResponse(BaseModel):
    code: str
    msg: str
    data: List[CompanyItem]

# 定义分页查询请求模型
class CompanyPageRequest(BaseModel):
    companyName: Optional[str] = ""
    pageNo: Optional[int] = 0  
    pageSize: Optional[int] = 0  
    tenantId: Optional[int] = None

# 定义分页查询结果项模型
class CompanyDetailItem(BaseModel):
    id: int
    tenantId: int
    tenantName: str
    name: str
    description: Optional[str] = None
    createTime: Optional[str] = None
    updateTime: Optional[str] = None
    operatorName: Optional[str] = None

# 定义分页数据模型
class PageData(BaseModel):
    records: List[CompanyDetailItem]
    total: int
    size: int
    current: int
    pages: int

# 定义分页查询响应模型
class CompanyPageResponse(BaseModel):
    code: str
    msg: str
    data: PageData

# 定义新增局点请求模型
class CompanyAddRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    tenantId: int

# 定义新增局点响应模型
class CompanyAddResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义修改局点请求模型
class CompanyModifyRequest(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    tenantId: Optional[int] = None

# 定义修改局点响应模型
class CompanyModifyResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义删除局点响应模型
class CompanyDeleteResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义网格列表项模型
class GridItem(BaseModel):
    id: int
    name: str

# 网格列表响应模型
class GridListResponse(BaseModel):
    code: str
    msg: str
    data: List[GridItem]

# 定义网格分页查询结果项模型
class GridDetailItem(BaseModel):
    id: int
    gridName: str
    companyId: int
    companyName: str
    tenantId: int
    tenantName: str
    createTime: Optional[str] = None
    updateTime: Optional[str] = None
    operatorName: Optional[str] = None

# 定义网格分页数据模型
class GridPageData(BaseModel):
    records: List[GridDetailItem]
    total: int
    size: int
    current: int
    pages: int

# 定义网格分页查询响应模型
class GridPageResponse(BaseModel):
    code: str
    msg: str
    data: GridPageData

# 定义小区详情项模型
class CommunityDetailItem(BaseModel):
    id: int
    name: str
    gridId: int
    gridName: str
    companyId: int
    companyName: str
    tenantId: int
    tenantName: str
    createTime: Optional[str] = None
    updateTime: Optional[str] = None
    operatorName: Optional[str] = None

# 定义小区分页数据模型
class CommunityPageData(BaseModel):
    records: List[CommunityDetailItem]
    total: int
    size: int
    current: int
    pages: int

# 定义小区分页查询响应模型
class CommunityPageResponse(BaseModel):
    code: str
    msg: str
    data: CommunityPageData

# 定义新增小区请求模型
class CommunityAddRequest(BaseModel):
    gridId: int
    name: str

# 定义新增小区响应模型
class CommunityAddResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义修改小区请求模型
class CommunityModifyRequest(BaseModel):
    id: int
    gridId: Optional[int] = None
    name: Optional[str] = None

# 定义修改小区响应模型
class CommunityModifyResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义删除小区响应模型
class CommunityDeleteResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义新增网格请求模型
class GridAddRequest(BaseModel):
    companyId: int
    name: str

# 定义新增网格响应模型
class GridAddResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义修改网格请求模型
class GridModifyRequest(BaseModel):
    id: int
    companyId: Optional[int] = None
    name: Optional[str] = None

# 定义修改网格响应模型
class GridModifyResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义删除网格响应模型
class GridDeleteResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义营销组详情项模型
class GroupDetailItem(BaseModel):
    id: int
    groupName: str
    description: Optional[str] = None
    companyId: int
    companyName: str
    tenantId: int
    tenantName: str
    createTime: Optional[str] = None
    updateTime: Optional[str] = None
    operatorName: Optional[str] = None

# 定义营销组分页数据模型
class GroupPageData(BaseModel):
    records: List[GroupDetailItem]
    total: int
    size: int
    current: int
    pages: int

# 定义营销组分页查询响应模型
class GroupPageResponse(BaseModel):
    code: str
    msg: str
    data: GroupPageData

# 定义新增营销组请求模型
class GroupAddRequest(BaseModel):
    companyId: int
    name: str
    description: Optional[str] = ""

# 定义新增营销组响应模型
class GroupAddResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义修改营销组请求模型
class GroupModifyRequest(BaseModel):
    id: int
    companyId: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None

# 定义修改营销组响应模型
class GroupModifyResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义删除营销组响应模型
class GroupDeleteResponse(BaseModel):
    code: str
    msg: str
    data: dict = None

# 定义营销组简单项模型（用于树形结构）
class GroupItemVO(BaseModel):
    id: int
    name: str

# 定义营销组树形结构响应模型
class GroupTreeResponse(BaseModel):
    code: str
    msg: str
    data: Optional[dict] = None

# 定义角色项模型
class RoleItem(BaseModel):
    id: int
    name: str

# 定义角色列表响应模型
class RoleListResponse(BaseModel):
    code: str
    msg: str
    data: List[RoleItem]

# 定义角色详情项模型
class RoleDetailItem(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    createTime: Optional[str] = None
    updateTime: Optional[str] = None
    operatorName: Optional[str] = None

# 定义角色分页数据模型
class RolePageData(BaseModel):
    records: List[RoleDetailItem]
    total: int
    size: int
    current: int
    pages: int

# 定义角色分页查询响应模型
class RolePageResponse(BaseModel):
    code: str
    msg: str
    data: RolePageData

# 定义角色分页查询请求模型
class RolePageRequest(BaseModel):
    name: Optional[str] = ""
    pageNo: Optional[int] = 0  
    pageSize: Optional[int] = 0  

# 定义新增角色请求模型
class RoleAddRequest(BaseModel):
    name: str
    description: Optional[str] = ""

# 定义新增角色响应模型
class RoleAddResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义修改角色请求模型
class RoleModifyRequest(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None

# 定义修改角色响应模型
class RoleModifyResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义删除角色响应模型
class RoleDeleteResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义标签类别常量
LABEL_TYPE = {
    1: "基础标签",
    2: "高级标签"
}

# 定义标签列表项模型
class LabelItem(BaseModel):
    id: int
    name: str
    type: int
    typeValue: str
    companyIds: str
    companyNames: str

# 定义标签分页数据模型
class LabelPageData(BaseModel):
    records: List[LabelItem]
    total: int
    size: int
    current: int
    pages: int

# 定义标签分页查询响应模型
class LabelPageResponse(BaseModel):
    code: str
    msg: str
    data: LabelPageData

# 定义标签分页查询请求模型
class LabelPageRequest(BaseModel):
    companyId: Optional[int] = 0
    name: Optional[str] = ""
    pageNo: Optional[int] = 0  
    pageSize: Optional[int] = 0  
    type: Optional[int] = 0

# 定义新增标签请求模型
class LabelAddRequest(BaseModel):
    name: str
    type: int

# 定义新增标签响应模型
class LabelAddResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义修改标签请求模型
class LabelModifyRequest(BaseModel):
    id: int
    name: Optional[str] = None
    type: Optional[int] = None

# 定义修改标签响应模型
class LabelModifyResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义删除标签响应模型
class LabelDeleteResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 定义配置标签局点请求模型
class LabelConfigureRequest(BaseModel):
    id: int
    companyList: List[int]

# 定义配置标签局点响应模型
class LabelConfigureResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 用户注册端点
@app.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 检查用户是否已存在
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # 创建新用户
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 创建访问令牌
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 登录端点
@app.post("/ces/sys/account/login", response_model=CommonResponse)
async def login(request: LoginRequest):
    # 只接受特定的用户名和密码
    if request.username != "zxjy" or request.password != "zxjy":
        return CommonResponse(
            code="A0001",
            msg="用户名或密码错误",
            data=None
        )

    # 创建访问令牌
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": request.username},
        expires_delta=access_token_expires
    )

    return CommonResponse(
        code="00000",
        msg="成功",
        data=access_token
    )

# 运营商列表查询接口
@app.post("/ces/tenant/list", response_model=TenantListResponse)
async def tenant_list(db: Session = Depends(get_db)):
    """
    查询运营商列表
    
    返回所有可用的运营商（租户）数据
    """
    try:
        # 从数据库查询租户信息
        tenants = db.query(models.Tenant).all()
        
        # 构建响应数据
        result = [{"id": tenant.id, "name": tenant.name} for tenant in tenants]
        
        return TenantListResponse(
            code="00000",
            msg="成功",
            data=result
        )
    except Exception as e:
        # 处理异常
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        # 记录错误日志
        print(f"Error in tenant_list: {error_msg}")
        print(f"Trace: {error_trace}")
        
        # 返回错误响应
        return TenantListResponse(
            code="A0002",
            msg=f"服务器错误: {error_msg}",
            data=[]
        )

# 公司/局点列表查询接口 - POST方法，直接处理原始请求
@app.post("/ces/company/list")
async def company_list(request: Request, db: Session = Depends(get_db)):
    """
    获取局点列表，支持按租户ID筛选
    - 如果不传递租户ID或传空字符串，则返回所有局点
    - 如果传递有效的租户ID，则返回对应租户的局点
    
    请求示例:
    {
        "tenantId": "" 或 "0" 或 1 或 "1"
    }
    """
    # 手动解析请求体，避免FastAPI的验证
    try:
        # 读取请求体
        body_bytes = await request.body()
        
        # 如果存在请求体，则解析JSON
        if body_bytes:
            import json
            try:
                body = json.loads(body_bytes)
                tenant_id_raw = body.get("tenantId", None)
            except json.JSONDecodeError:
                # JSON解析失败
                tenant_id_raw = None
        else:
            # 没有请求体
            tenant_id_raw = None
    except Exception:
        # 任何错误都默认为不筛选
        tenant_id_raw = None
    
    # 构建查询
    query = db.query(models.Company)
    
    # 根据tenantId筛选
    # 只有当tenantId不为None、空字符串、"0"或0时才筛选
    if tenant_id_raw not in [None, "", "0", 0]:
        try:
            # 尝试转换为整数
            tenant_id = int(tenant_id_raw)
            query = query.filter(models.Company.tenant_id == tenant_id)
        except (ValueError, TypeError):
            # 转换失败，返回所有局点
            pass
    
    # 执行查询
    companies = query.all()
    
    # 构建响应
    result = [{"id": company.id, "name": company.name} for company in companies]
    
    # 返回响应
    return JSONResponse(content={
        "code": "00000",
        "msg": "成功",
        "data": result
    })

# 公司/局点列表查询接口 - GET方法，支持路径参数
@app.get("/ces/company/list/{tenant_id}", response_model=CompanyListResponse)
async def company_list_by_path(tenant_id: str = "0", db: Session = Depends(get_db)):
    """
    通过路径参数获取局点列表
    例如：/ces/company/list/1 获取租户ID为1的局点
         /ces/company/list/0 获取所有局点
    """
    # 构建查询
    query = db.query(models.Company)
    
    # 根据tenant_id筛选
    if tenant_id not in ["0", ""]:
        try:
            tid = int(tenant_id)
            query = query.filter(models.Company.tenant_id == tid)
        except (ValueError, TypeError):
            # 无效的ID，返回所有结果
            pass
    
    # 执行查询
    companies = query.all()
    
    # 构建响应
    result = [{"id": company.id, "name": company.name} for company in companies]
    
    return CompanyListResponse(
        code="00000",
        msg="成功",
        data=result
    )

# 公司/局点列表查询接口 - GET方法，支持查询参数
@app.get("/ces/company/list", response_model=CompanyListResponse)
async def company_list_by_query(tenant_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    通过查询参数获取局点列表
    例如：/ces/company/list?tenant_id=1 获取租户ID为1的局点
         /ces/company/list 获取所有局点
    """
    # 构建查询
    query = db.query(models.Company)
    
    # 根据tenant_id筛选
    if tenant_id not in [None, "", "0"]:
        try:
            tid = int(tenant_id)
            query = query.filter(models.Company.tenant_id == tid)
        except (ValueError, TypeError):
            # 无效的ID，返回所有结果
            pass
    
    # 执行查询
    companies = query.all()
    
    # 构建响应
    result = [{"id": company.id, "name": company.name} for company in companies]
    
    return CompanyListResponse(
        code="00000",
        msg="成功",
        data=result
    )

# 公司/局点分页查询接口
@app.post("/ces/company/list/page")
async def company_list_page(request: Request, db: Session = Depends(get_db)):
    """
    局点分页查询接口，支持按租户ID筛选、公司名称筛选和分页
    
    请求示例:
    {
        "companyName": "",
        "pageNo": 1,
        "pageSize": 10,
        "tenantId": 0
    }
    
    - 如果pageNo和pageSize都为0，返回所有结果
    - 支持按公司名称模糊查询
    - 支持按租户ID筛选
    """
    # 手动解析请求体，避免FastAPI的验证
    try:
        body_bytes = await request.body()
        
        if body_bytes:
            import json
            try:
                body = json.loads(body_bytes)
                company_name = body.get("companyName", "")
                page_no = body.get("pageNo", 1)
                page_size = body.get("pageSize", 10)
                tenant_id = body.get("tenantId", None)
            except json.JSONDecodeError:
                company_name = ""
                page_no = 1
                page_size = 10
                tenant_id = None
        else:
            company_name = ""
            page_no = 1
            page_size = 10
            tenant_id = None
    except Exception:
        company_name = ""
        page_no = 1
        page_size = 10
        tenant_id = None
    
    try:
        # 只查询已知存在的列: id, name, tenant_id
        query = db.query(models.Company.id, models.Company.name, models.Company.tenant_id)
        
        # 应用过滤条件：公司名称模糊查询
        if company_name:
            query = query.filter(models.Company.name.like(f'%{company_name}%'))
        
        # 应用过滤条件：租户ID
        if tenant_id and tenant_id not in [0]:
            query = query.filter(models.Company.tenant_id == tenant_id)
        
        # 获取总记录数，只计算id列
        total_query = db.query(models.Company.id)
        if company_name:
            total_query = total_query.filter(models.Company.name.like(f'%{company_name}%'))
        if tenant_id and tenant_id not in [0]:
            total_query = total_query.filter(models.Company.tenant_id == tenant_id)
        
        total_records = total_query.count()
        
        # 分页处理
        if page_no > 0 and page_size > 0:
            query = query.offset((page_no - 1) * page_size).limit(page_size)
            current_page = page_no
            page_size = page_size
            total_pages = math.ceil(total_records / page_size) if page_size > 0 else 1
        else:
            # 不分页，返回所有记录
            current_page = 1
            page_size = total_records
            total_pages = 1
        
        # 执行查询
        companies = query.all()
        
        # 构建响应数据，使用硬编码值替代不存在的列
        records = []
        for company in companies:
            # 查询租户名称
            tenant = db.query(models.Tenant).filter(models.Tenant.id == company.tenant_id).first()
            tenant_name = tenant.name if tenant else "未知租户"
            
            records.append({
                "id": company.id,
                "tenantId": company.tenant_id,
                "tenantName": tenant_name,
                "name": company.name,
                # 以下使用硬编码值代替数据库中不存在的列
                "description": f"这是{company.name}的描述",
                "createTime": "2023-03-20 10:00:00",
                "updateTime": "2023-03-22 14:30:00" if company.id % 2 == 0 else None,
                "operatorName": "管理员" if company.id % 2 == 0 else "test3" if company.id % 3 == 0 else None
            })
        
        # 返回成功响应
        return JSONResponse(content={
            "code": "00000",
            "msg": "成功",
            "data": {
                "records": records,
                "total": total_records,
                "size": page_size,
                "current": current_page,
                "pages": total_pages
            }
        })
    except Exception as e:
        # 捕获所有异常并返回友好的错误信息
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error in company_list_page: {str(e)}\n{error_detail}")
        
        return JSONResponse(
            status_code=200,  # 使用200而不是500，客户端更友好
            content={
                "code": "A0500",
                "msg": f"服务器内部错误: {str(e)}",
                "data": {
                    "records": [],
                    "total": 0,
                    "size": page_size,
                    "current": page_no,
                    "pages": 0
                }
            }
        )

# 新增局点接口
@app.post("/ces/company/add", response_model=CompanyAddResponse)
async def company_add(request: Request, db: Session = Depends(get_db)):
    """
    新增局点接口
    
    请求示例:
    {
        "name": "新局点名称",
        "description": "局点描述",
        "tenantId": 1
    }
    """
    try:
        # 读取请求体
        body_bytes = await request.body()
        
        # 解析JSON
        if not body_bytes:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体不能为空",
                    "data": {}
                }
            )
            
        import json
        try:
            body = json.loads(body_bytes)
            name = body.get("name")
            description = body.get("description", "")  # 仍然接收description，但不会存储到数据库
            tenant_id = body.get("tenantId")
        except json.JSONDecodeError:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体格式错误",
                    "data": {}
                }
            )
        
        # 验证必填字段
        if not name:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "局点名称不能为空",
                    "data": {}
                }
            )
            
        if tenant_id is None:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "租户ID不能为空",
                    "data": {}
                }
            )
        
        # 验证租户是否存在
        tenant = db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()
        if not tenant:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": f"租户ID {tenant_id} 不存在",
                    "data": {}
                }
            )
            
        # 创建新局点 - 仅使用实际存在的数据库列
        new_company = models.Company(
            name=name,
            tenant_id=tenant_id
            # 忽略不存在的列: description, create_time, update_time, operator_name
        )
        
        # 保存到数据库
        db.add(new_company)
        db.commit()
        db.refresh(new_company)
        
        # 返回成功响应 - 返回数据中仍然包含前端期望的字段
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": {
                    "id": new_company.id,
                    "name": new_company.name,
                    "description": description,  # 使用请求中的description，而不是从数据库读取
                    "tenantId": new_company.tenant_id,
                    "createTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 使用当前时间
                }
            }
        )
        
    except Exception as e:
        # 处理异常
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        # 记录错误日志（实际应用中应该使用日志模块）
        print(f"Error: {error_msg}")
        print(f"Trace: {error_trace}")
        
        # 返回错误响应
        return JSONResponse(
            content={
                "code": "A0002",
                "msg": f"服务器错误: {error_msg}",
                "data": {}
            }
        )

# 修改局点接口
@app.post("/ces/company/modify", response_model=CompanyModifyResponse)
async def company_modify(request: Request, db: Session = Depends(get_db)):
    """
    修改局点接口
    
    请求示例:
    {
        "id": 1,
        "name": "更新的局点名称",
        "description": "更新的局点描述",
        "tenantId": 1
    }
    """
    try:
        # 读取请求体
        body_bytes = await request.body()
        
        # 解析JSON
        if not body_bytes:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体不能为空",
                    "data": {}
                }
            )
            
        import json
        try:
            body = json.loads(body_bytes)
            company_id = body.get("id")
            name = body.get("name")
            description = body.get("description")  # 仍然接收description，但不会存储到数据库
            tenant_id = body.get("tenantId")
        except json.JSONDecodeError:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体格式错误",
                    "data": {}
                }
            )
        
        # 验证必填字段
        if company_id is None:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "局点ID不能为空",
                    "data": {}
                }
            )
        
        # 查询要修改的局点
        company = db.query(models.Company).filter(models.Company.id == company_id).first()
        if not company:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": f"局点ID {company_id} 不存在",
                    "data": {}
                }
            )
        
        # 如果提供了新的租户ID，验证租户是否存在
        if tenant_id is not None:
            tenant = db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()
            if not tenant:
                return JSONResponse(
                    content={
                        "code": "A0001", 
                        "msg": f"租户ID {tenant_id} 不存在",
                        "data": {}
                    }
                )
            company.tenant_id = tenant_id
        
        # 更新局点信息 - 只更新实际存在的列
        if name is not None:
            if not name.strip():  # 检查名称不能为空或只包含空格
                return JSONResponse(
                    content={
                        "code": "A0001", 
                        "msg": "局点名称不能为空",
                        "data": {}
                    }
                )
            company.name = name
            
        # 不设置description，因为数据库中不存在该列
        # 不设置update_time和operator_name，因为数据库中不存在这些列
        
        # 保存到数据库
        db.commit()
        db.refresh(company)
        
        # 获取租户名称
        tenant = db.query(models.Tenant).filter(models.Tenant.id == company.tenant_id).first()
        tenant_name = tenant.name if tenant else "未知租户"
        
        # 返回成功响应 - 返回数据中仍然包含前端期望的字段
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": {
                    "id": company.id,
                    "name": company.name,
                    "description": description if description is not None else "",  # 使用请求中的description
                    "tenantId": company.tenant_id,
                    "tenantName": tenant_name,
                    "createTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 使用当前时间
                    "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 使用当前时间
                    "operatorName": "管理员"  # 硬编码
                }
            }
        )
        
    except Exception as e:
        # 处理异常
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        # 记录错误日志（实际应用中应该使用日志模块）
        print(f"Error: {error_msg}")
        print(f"Trace: {error_trace}")
        
        # 返回错误响应
        return JSONResponse(
            content={
                "code": "A0002",
                "msg": f"服务器错误: {error_msg}",
                "data": {}
            }
        )

# 删除局点接口
@app.delete("/ces/company/delete", response_model=CompanyDeleteResponse)
async def company_delete(id: int, db: Session = Depends(get_db)):
    """
    删除局点接口
    
    示例：DELETE /ces/company/delete?id=1 删除ID为1的局点
    """
    try:
        # 查询要删除的局点
        company = db.query(models.Company).filter(models.Company.id == id).first()
        
        # 如果局点不存在，返回错误
        if not company:
            return JSONResponse(
                content={
                    "code": "A0001",
                    "msg": f"局点ID {id} 不存在",
                    "data": {}
                }
            )
        
        # 保存局点信息用于返回
        company_info = {
            "id": company.id,
            "name": company.name,
            "tenantId": company.tenant_id
        }
        
        # 删除局点
        db.delete(company)
        db.commit()
        
        # 返回成功响应
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": company_info
            }
        )
        
    except Exception as e:
        # 处理异常
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        # 记录错误日志
        print(f"Error: {error_msg}")
        print(f"Trace: {error_trace}")
        
        # 返回错误响应
        return JSONResponse(
            content={
                "code": "A0002",
                "msg": f"服务器错误: {error_msg}",
                "data": {}
            }
        )

# 网格列表查询接口
@app.post("/ces/grid/list", response_model=GridListResponse)
async def grid_list(request: Request, db: Session = Depends(get_db)):
    """
    获取网格列表，支持按局点ID筛选
    - 如果不传递局点ID或传0，则返回所有网格
    - 如果传递有效的局点ID，则返回对应局点的网格
    
    请求示例:
    {
        "companyId": 0 或 1 或 "1"
    }
    """
    try:
        # 读取请求体
        body_bytes = await request.body()
        
        # 解析JSON
        if not body_bytes:
            company_id = 0  # 默认查询所有
        else:
            import json
            try:
                body = json.loads(body_bytes)
                company_id = body.get("companyId", 0)
            except json.JSONDecodeError:
                company_id = 0  # JSON解析失败，默认查询所有
        
        # 构建查询
        query = db.query(models.Grid)
        
        # 根据companyId筛选
        # 只有当companyId不为0时才筛选
        if company_id != 0:
            try:
                # 尝试转换为整数
                company_id = int(company_id)
                # 先检查公司是否存在
                company = db.query(models.Company).filter(models.Company.id == company_id).first()
                if not company:
                    return JSONResponse(
                        content={
                            "code": "A0001", 
                            "msg": f"局点ID {company_id} 不存在",
                            "data": []
                        }
                    )
                # 筛选指定局点的网格
                query = query.filter(models.Grid.company_id == company_id)
            except (ValueError, TypeError):
                # 转换失败，返回所有网格
                pass
        
        # 执行查询
        grids = query.all()
        
        # 构建响应
        result = [{"id": grid.id, "name": grid.name} for grid in grids]
        
        # 返回响应
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": result
            }
        )
    
    except Exception as e:
        # 处理异常
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        # 记录错误日志
        print(f"Error: {error_msg}")
        print(f"Trace: {error_trace}")
        
        # 返回错误响应
        return JSONResponse(
            content={
                "code": "A0002",
                "msg": f"服务器错误: {error_msg}",
                "data": []
            }
        )

# 网格分页查询接口
@app.post("/ces/grid/list/page")
async def grid_list_page(request: Request, db: Session = Depends(get_db)):
    """
    网格分页查询接口，支持按租户ID、公司ID、网格名称筛选和分页
    
    请求示例:
    {
        "companyId": 0,
        "name": "",
        "pageNo": 1,
        "pageSize": 10,
        "tenantId": 0
    }
    
    - 如果companyId为0，查询所有公司的网格
    - 如果tenantId为0，查询所有租户的网格
    - 支持按网格名称模糊查询
    - 支持分页功能
    """
    try:
        # 读取请求体
        body_bytes = await request.body()
        
        # 解析JSON请求
        if not body_bytes:
            company_id = 0
            grid_name = ""
            page_no = 1
            page_size = 10
            tenant_id = 0
        else:
            import json
            try:
                body = json.loads(body_bytes)
                company_id = body.get("companyId", 0)
                grid_name = body.get("name", "")
                page_no = body.get("pageNo", 1)
                page_size = body.get("pageSize", 10)
                tenant_id = body.get("tenantId", 0)
            except json.JSONDecodeError:
                company_id = 0
                grid_name = ""
                page_no = 1
                page_size = 10
                tenant_id = 0
        
        # 创建基础查询，包含网格和关联的公司信息
        query = db.query(
            models.Grid.id,
            models.Grid.name.label("grid_name"),
            models.Grid.company_id,
            models.Company.name.label("company_name"),
            models.Company.tenant_id,
            models.Tenant.name.label("tenant_name")
        ).join(
            models.Company, models.Grid.company_id == models.Company.id
        ).join(
            models.Tenant, models.Company.tenant_id == models.Tenant.id
        )
        
        # 应用过滤条件：网格名称模糊查询
        if grid_name:
            query = query.filter(models.Grid.name.like(f'%{grid_name}%'))
        
        # 应用过滤条件：公司ID
        if company_id and company_id != 0:
            query = query.filter(models.Grid.company_id == company_id)
        
        # 应用过滤条件：租户ID
        if tenant_id and tenant_id != 0:
            query = query.filter(models.Company.tenant_id == tenant_id)
        
        # 获取总记录数，创建一个复制的查询以计算总数
        total_query = query
        total_records = total_query.count()
        
        # 分页处理
        if page_no > 0 and page_size > 0:
            query = query.offset((page_no - 1) * page_size).limit(page_size)
            current_page = page_no
            page_size = page_size
            total_pages = math.ceil(total_records / page_size) if page_size > 0 else 1
        else:
            # 不分页，返回所有记录
            current_page = 1
            page_size = total_records
            total_pages = 1
        
        # 执行查询
        grid_results = query.all()
        
        # 构建响应数据，添加前端期望的其他字段
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        records = []
        
        for grid in grid_results:
            records.append({
                "id": grid.id,
                "gridName": grid.grid_name,
                "companyId": grid.company_id,
                "companyName": grid.company_name,
                "tenantId": grid.tenant_id,
                "tenantName": grid.tenant_name,
                # 以下字段在数据库中不存在，使用硬编码值
                "createTime": current_time,
                "updateTime": current_time if grid.id % 2 == 0 else None,
                "operatorName": "管理员" if grid.id % 2 == 0 else "操作员" if grid.id % 3 == 0 else None
            })
        
        # 返回成功响应
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": {
                    "records": records,
                    "total": total_records,
                    "size": page_size,
                    "current": current_page,
                    "pages": total_pages
                }
            }
        )
        
    except Exception as e:
        # 捕获所有异常并返回友好的错误信息
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error in grid_list_page: {str(e)}\n{error_detail}")
        
        return JSONResponse(
            status_code=200,  # 使用200而不是500，客户端更友好
            content={
                "code": "A0500",
                "msg": f"服务器内部错误: {str(e)}",
                "data": {
                    "records": [],
                    "total": 0,
                    "size": page_size if 'page_size' in locals() else 10,
                    "current": page_no if 'page_no' in locals() else 1,
                    "pages": 0
                }
            }
        )

# 新增网格接口
@app.post("/ces/grid/add", response_model=GridAddResponse)
async def grid_add(request: Request, db: Session = Depends(get_db)):
    """
    新增网格接口
    
    请求示例:
    {
        "companyId": 1,
        "name": "新网格名称"
    }
    """
    try:
        # 读取请求体
        body_bytes = await request.body()
        
        # 解析JSON
        if not body_bytes:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体不能为空",
                    "data": {}
                }
            )
            
        import json
        try:
            body = json.loads(body_bytes)
            company_id = body.get("companyId")
            name = body.get("name")
        except json.JSONDecodeError:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体格式错误",
                    "data": {}
                }
            )
        
        # 验证必填字段
        if company_id is None:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "局点ID不能为空",
                    "data": {}
                }
            )
            
        if not name:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "网格名称不能为空",
                    "data": {}
                }
            )
        
        # 验证局点是否存在
        company = db.query(models.Company).filter(models.Company.id == company_id).first()
        if not company:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": f"局点ID {company_id} 不存在",
                    "data": {}
                }
            )
        
        # 查询关联的租户信息
        tenant = db.query(models.Tenant).filter(models.Tenant.id == company.tenant_id).first()
        
        # 创建新网格
        new_grid = models.Grid(
            name=name,
            company_id=company_id
        )
        
        # 保存到数据库
        db.add(new_grid)
        db.commit()
        db.refresh(new_grid)
        
        # 返回成功响应
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": {
                    "id": new_grid.id,
                    "name": new_grid.name,
                    "companyId": new_grid.company_id,
                    "companyName": company.name,
                    "tenantId": company.tenant_id,
                    "tenantName": tenant.name if tenant else "未知租户",
                    "createTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
        )
        
    except Exception as e:
        # 处理异常
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        # 记录错误日志
        print(f"Error in grid_add: {error_msg}")
        print(f"Trace: {error_trace}")
        
        # 返回错误响应
        return JSONResponse(
            content={
                "code": "A0002",
                "msg": f"服务器错误: {error_msg}",
                "data": {}
            }
        )

# 修改网格接口
@app.post("/ces/grid/modify", response_model=GridModifyResponse)
async def grid_modify(request: Request, db: Session = Depends(get_db)):
    """
    修改网格接口
    
    请求示例:
    {
        "id": 1,
        "companyId": 2,
        "name": "修改后的网格名称"
    }
    """
    try:
        # 读取请求体
        body_bytes = await request.body()
        
        # 解析JSON
        if not body_bytes:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体不能为空",
                    "data": {}
                }
            )
            
        import json
        try:
            body = json.loads(body_bytes)
            grid_id = body.get("id")
            company_id = body.get("companyId")
            name = body.get("name")
        except json.JSONDecodeError:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体格式错误",
                    "data": {}
                }
            )
        
        # 验证必填字段
        if grid_id is None:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "网格ID不能为空",
                    "data": {}
                }
            )
        
        # 查询要修改的网格
        grid = db.query(models.Grid).filter(models.Grid.id == grid_id).first()
        if not grid:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": f"网格ID {grid_id} 不存在",
                    "data": {}
                }
            )
        
        # 准备修改后的数据 - 默认使用原有数据
        updated_company_id = grid.company_id
        updated_name = grid.name
        
        # 如果提供了新的公司ID，验证公司是否存在并更新
        if company_id is not None:
            company = db.query(models.Company).filter(models.Company.id == company_id).first()
            if not company:
                return JSONResponse(
                    content={
                        "code": "A0001", 
                        "msg": f"局点ID {company_id} 不存在",
                        "data": {}
                    }
                )
            updated_company_id = company_id
        
        # 如果提供了新的名称，检查并更新
        if name is not None:
            if not name.strip():  # 检查名称不能为空或只包含空格
                return JSONResponse(
                    content={
                        "code": "A0001", 
                        "msg": "网格名称不能为空",
                        "data": {}
                    }
                )
            updated_name = name
        
        # 更新网格信息
        grid.company_id = updated_company_id
        grid.name = updated_name
        
        # 保存到数据库
        db.commit()
        db.refresh(grid)
        
        # 获取更新后的关联信息
        company = db.query(models.Company).filter(models.Company.id == grid.company_id).first()
        tenant = None
        if company:
            tenant = db.query(models.Tenant).filter(models.Tenant.id == company.tenant_id).first()
        
        # 返回成功响应
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": {
                    "id": grid.id,
                    "name": grid.name,
                    "companyId": grid.company_id,
                    "companyName": company.name if company else "未知公司",
                    "tenantId": company.tenant_id if company else 0,
                    "tenantName": tenant.name if tenant else "未知租户",
                    "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
        )
        
    except Exception as e:
        # 处理异常
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        # 记录错误日志
        print(f"Error in grid_modify: {error_msg}")
        print(f"Trace: {error_trace}")
        
        # 返回错误响应
        return JSONResponse(
            content={
                "code": "A0002",
                "msg": f"服务器错误: {error_msg}",
                "data": {}
            }
        )

# 删除网格接口
@app.delete("/ces/grid/delete", response_model=GridDeleteResponse)
async def grid_delete(id: int, db: Session = Depends(get_db)):
    """
    删除网格接口
    
    示例：DELETE /ces/grid/delete?id=1 删除ID为1的网格
    """
    try:
        # 查询要删除的网格
        grid = db.query(models.Grid).filter(models.Grid.id == id).first()
        
        # 如果网格不存在，返回错误
        if not grid:
            return JSONResponse(
                content={
                    "code": "A0001",
                    "msg": f"网格ID {id} 不存在",
                    "data": {}
                }
            )
        
        # 获取公司和租户信息，用于返回
        company = db.query(models.Company).filter(models.Company.id == grid.company_id).first()
        tenant = None
        if company:
            tenant = db.query(models.Tenant).filter(models.Tenant.id == company.tenant_id).first()
            
        # 保存网格信息用于返回
        grid_info = {
            "id": grid.id,
            "name": grid.name,
            "companyId": grid.company_id,
            "companyName": company.name if company else "未知公司",
            "tenantId": company.tenant_id if company else 0,
            "tenantName": tenant.name if tenant else "未知租户"
        }
        
        # 删除网格
        db.delete(grid)
        db.commit()
        
        # 返回成功响应
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": grid_info
            }
        )
        
    except Exception as e:
        # 处理异常
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        # 记录错误日志
        print(f"Error in grid_delete: {error_msg}")
        print(f"Trace: {error_trace}")
        
        # 返回错误响应
        return JSONResponse(
            content={
                "code": "A0002",
                "msg": f"服务器错误: {error_msg}",
                "data": {}
            }
        )

# 小区分页查询接口
@app.post("/ces/community/list/page", response_model=CommunityPageResponse)
async def community_list_page(request: Request, db: Session = Depends(get_db)):
    """
    小区分页查询接口，支持按租户ID、公司ID、网格ID、小区名称筛选和分页
    
    请求示例:
    {
        "companyId": 0,  // 局点id
        "gridId": 0,     // 网格id
        "name": "",      // 小区名称
        "pageNo": 1,
        "pageSize": 10,
        "tenantId": 0    // 运营商id
    }
    
    - 如果companyId为0，查询所有公司的小区
    - 如果gridId为0，查询所有网格的小区
    - 如果tenantId为0，查询所有租户的小区
    - 支持按小区名称模糊查询
    - 支持分页功能
    """
    try:
        # 读取请求体
        body_bytes = await request.body()
        
        # 解析JSON请求
        if not body_bytes:
            company_id = 0
            grid_id = 0
            community_name = ""
            page_no = 1
            page_size = 10
            tenant_id = 0
        else:
            import json
            try:
                body = json.loads(body_bytes)
                company_id = body.get("companyId", 0)
                grid_id = body.get("gridId", 0)
                community_name = body.get("name", "")
                page_no = body.get("pageNo", 1)
                page_size = body.get("pageSize", 10)
                tenant_id = body.get("tenantId", 0)
            except json.JSONDecodeError:
                company_id = 0
                grid_id = 0
                community_name = ""
                page_no = 1
                page_size = 10
                tenant_id = 0
        
        # 创建基础查询，包含小区和关联的网格、公司、租户信息
        query = db.query(
            models.Community.id,
            models.Community.name,
            models.Community.grid_id,
            models.Community.create_time,
            models.Community.update_time,
            models.Community.operator_name,
            models.Grid.name.label("grid_name"),
            models.Grid.company_id,
            models.Company.name.label("company_name"),
            models.Company.tenant_id,
            models.Tenant.name.label("tenant_name")
        ).join(
            models.Grid, models.Community.grid_id == models.Grid.id
        ).join(
            models.Company, models.Grid.company_id == models.Company.id
        ).join(
            models.Tenant, models.Company.tenant_id == models.Tenant.id
        )
        
        # 应用过滤条件：小区名称模糊查询
        if community_name:
            query = query.filter(models.Community.name.like(f'%{community_name}%'))
        
        # 应用过滤条件：网格ID
        if grid_id and grid_id != 0:
            query = query.filter(models.Community.grid_id == grid_id)
        
        # 应用过滤条件：公司ID
        if company_id and company_id != 0:
            query = query.filter(models.Grid.company_id == company_id)
        
        # 应用过滤条件：租户ID
        if tenant_id and tenant_id != 0:
            query = query.filter(models.Company.tenant_id == tenant_id)
        
        # 获取总记录数，创建一个复制的查询以计算总数
        total_query = query
        total_records = total_query.count()
        
        # 分页处理
        if page_no > 0 and page_size > 0:
            query = query.offset((page_no - 1) * page_size).limit(page_size)
            current_page = page_no
            page_size = page_size
            total_pages = math.ceil(total_records / page_size) if page_size > 0 else 1
        else:
            # 不分页，返回所有记录
            current_page = 1
            page_size = total_records
            total_pages = 1
        
        # 执行查询
        community_results = query.all()
        
        # 构建响应数据
        records = []
        
        for community in community_results:
            # 格式化日期时间
            create_time = community.create_time.strftime("%Y-%m-%d %H:%M:%S") if community.create_time else None
            update_time = community.update_time.strftime("%Y-%m-%d %H:%M:%S") if community.update_time else None
            
            records.append({
                "id": community.id,
                "name": community.name,
                "gridId": community.grid_id,
                "gridName": community.grid_name,
                "companyId": community.company_id,
                "companyName": community.company_name,
                "tenantId": community.tenant_id,
                "tenantName": community.tenant_name,
                "createTime": create_time,
                "updateTime": update_time,
                "operatorName": community.operator_name
            })
        
        # 返回成功响应
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": {
                    "records": records,
                    "total": total_records,
                    "size": page_size,
                    "current": current_page,
                    "pages": total_pages
                }
            }
        )
        
    except Exception as e:
        # 捕获所有异常并返回友好的错误信息
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error in community_list_page: {str(e)}\n{error_detail}")
        
        return JSONResponse(
            status_code=200,  # 使用200而不是500，客户端更友好
            content={
                "code": "A0500",
                "msg": f"服务器内部错误: {str(e)}",
                "data": {
                    "records": [],
                    "total": 0,
                    "size": page_size if 'page_size' in locals() else 10,
                    "current": page_no if 'page_no' in locals() else 1,
                    "pages": 0
                }
            }
        )

# 新增小区接口
@app.post("/ces/community/add", response_model=CommunityAddResponse)
async def community_add(request: Request, db: Session = Depends(get_db)):
    """
    新增小区接口
    
    请求示例:
    {
        "gridId": 1,  // 网格id
        "name": "新小区名称"
    }
    """
    try:
        # 读取请求体
        body_bytes = await request.body()
        
        # 解析JSON
        if not body_bytes:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体不能为空",
                    "data": {}
                }
            )
            
        import json
        try:
            body = json.loads(body_bytes)
            grid_id = body.get("gridId")
            name = body.get("name")
        except json.JSONDecodeError:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体格式错误",
                    "data": {}
                }
            )
        
        # 验证必填字段
        if grid_id is None:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "网格ID不能为空",
                    "data": {}
                }
            )
            
        if not name:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "小区名称不能为空",
                    "data": {}
                }
            )
        
        # 验证网格是否存在
        grid = db.query(models.Grid).filter(models.Grid.id == grid_id).first()
        if not grid:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": f"网格ID {grid_id} 不存在",
                    "data": {}
                }
            )
        
        # 查询关联的公司和租户信息
        company = db.query(models.Company).filter(models.Company.id == grid.company_id).first()
        tenant = None
        if company:
            tenant = db.query(models.Tenant).filter(models.Tenant.id == company.tenant_id).first()
        
        # 创建新小区
        current_time = datetime.now()
        new_community = models.Community(
            name=name,
            grid_id=grid_id,
            create_time=current_time,
            update_time=current_time,
            operator_name="管理员"  # 默认操作人
        )
        
        # 保存到数据库
        db.add(new_community)
        db.commit()
        db.refresh(new_community)
        
        # 返回成功响应
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": {
                    "id": new_community.id,
                    "name": new_community.name,
                    "gridId": new_community.grid_id,
                    "gridName": grid.name,
                    "companyId": company.id if company else 0,
                    "companyName": company.name if company else "未知公司",
                    "tenantId": company.tenant_id if company else 0,
                    "tenantName": tenant.name if tenant else "未知租户",
                    "createTime": new_community.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "updateTime": new_community.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "operatorName": new_community.operator_name
                }
            }
        )
        
    except Exception as e:
        # 处理异常
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        # 记录错误日志
        print(f"Error in community_add: {error_msg}")
        print(f"Trace: {error_trace}")
        
        # 返回错误响应
        return JSONResponse(
            content={
                "code": "A0002",
                "msg": f"服务器错误: {error_msg}",
                "data": {}
            }
        )

# 修改小区接口
@app.post("/ces/community/modify", response_model=CommunityModifyResponse)
async def community_modify(request: Request, db: Session = Depends(get_db)):
    """
    修改小区接口
    
    请求示例:
    {
        "id": 1,           // 小区id
        "gridId": 2,       // 网格id，可选
        "name": "新名称"    // 小区名称，可选
    }
    """
    try:
        # 读取请求体
        body_bytes = await request.body()
        
        # 解析JSON
        if not body_bytes:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体不能为空",
                    "data": {}
                }
            )
            
        import json
        try:
            body = json.loads(body_bytes)
            community_id = body.get("id")
            grid_id = body.get("gridId")
            name = body.get("name")
        except json.JSONDecodeError:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体格式错误",
                    "data": {}
                }
            )
        
        # 验证小区ID
        if community_id is None:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "小区ID不能为空",
                    "data": {}
                }
            )
        
        # 查询要修改的小区
        community = db.query(models.Community).filter(models.Community.id == community_id).first()
        if not community:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": f"小区ID {community_id} 不存在",
                    "data": {}
                }
            )
        
        # 原始网格ID
        original_grid_id = community.grid_id
        updated_grid_id = original_grid_id
        grid = db.query(models.Grid).filter(models.Grid.id == original_grid_id).first()
        
        # 如果提供了新的网格ID，验证网格是否存在
        if grid_id is not None:
            if grid_id != original_grid_id:
                new_grid = db.query(models.Grid).filter(models.Grid.id == grid_id).first()
                if not new_grid:
                    return JSONResponse(
                        content={
                            "code": "A0001", 
                            "msg": f"网格ID {grid_id} 不存在",
                            "data": {}
                        }
                    )
                updated_grid_id = grid_id
                grid = new_grid
        
        # 如果提供了新的名称，检查并更新
        if name is not None:
            if not name.strip():  # 检查名称不能为空或只包含空格
                return JSONResponse(
                    content={
                        "code": "A0001", 
                        "msg": "小区名称不能为空",
                        "data": {}
                    }
                )
            community.name = name
        
        # 更新网格ID
        community.grid_id = updated_grid_id
        
        # 更新修改时间
        community.update_time = datetime.now()
        
        # 保存到数据库
        db.commit()
        db.refresh(community)
        
        # 获取相关实体信息
        company = db.query(models.Company).filter(models.Company.id == grid.company_id).first()
        tenant = None
        if company:
            tenant = db.query(models.Tenant).filter(models.Tenant.id == company.tenant_id).first()
            
        # 返回成功响应
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": {
                    "id": community.id,
                    "name": community.name,
                    "gridId": community.grid_id,
                    "gridName": grid.name,
                    "companyId": company.id if company else 0,
                    "companyName": company.name if company else "未知公司",
                    "tenantId": company.tenant_id if company else 0,
                    "tenantName": tenant.name if tenant else "未知租户",
                    "createTime": community.create_time.strftime("%Y-%m-%d %H:%M:%S") if community.create_time else None,
                    "updateTime": community.update_time.strftime("%Y-%m-%d %H:%M:%S") if community.update_time else None,
                    "operatorName": community.operator_name
                }
            }
        )
        
    except Exception as e:
        # 处理异常
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        # 记录错误日志
        print(f"Error in community_modify: {error_msg}")
        print(f"Trace: {error_trace}")
        
        # 返回错误响应
        return JSONResponse(
            content={
                "code": "A0002",
                "msg": f"服务器错误: {error_msg}",
                "data": {}
            }
        )

# 删除小区接口
@app.delete("/ces/community/delete", response_model=CommunityDeleteResponse)
async def community_delete(id: int, db: Session = Depends(get_db)):
    """
    删除小区接口
    
    示例：DELETE /ces/community/delete?id=1 删除ID为1的小区
    """
    try:
        # 查询要删除的小区
        community = db.query(models.Community).filter(models.Community.id == id).first()
        
        # 如果小区不存在，返回错误
        if not community:
            return JSONResponse(
                content={
                    "code": "A0001",
                    "msg": f"小区ID {id} 不存在",
                    "data": {}
                }
            )
        
        # 获取关联的网格信息
        grid = db.query(models.Grid).filter(models.Grid.id == community.grid_id).first()
        company = None
        tenant = None
        
        if grid:
            company = db.query(models.Company).filter(models.Company.id == grid.company_id).first()
            if company:
                tenant = db.query(models.Tenant).filter(models.Tenant.id == company.tenant_id).first()
        
        # 保存小区信息用于返回
        community_info = {
            "id": community.id,
            "name": community.name,
            "gridId": community.grid_id,
            "gridName": grid.name if grid else "未知网格",
            "companyId": grid.company_id if grid else 0,
            "companyName": company.name if company else "未知公司",
            "tenantId": company.tenant_id if company else 0,
            "tenantName": tenant.name if tenant else "未知租户",
            "createTime": community.create_time.strftime("%Y-%m-%d %H:%M:%S") if community.create_time else None,
            "updateTime": community.update_time.strftime("%Y-%m-%d %H:%M:%S") if community.update_time else None,
            "operatorName": community.operator_name
        }
        
        # 删除小区
        db.delete(community)
        db.commit()
        
        # 返回成功响应
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": community_info
            }
        )
        
    except Exception as e:
        # 处理异常
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        # 记录错误日志
        print(f"Error in community_delete: {error_msg}")
        print(f"Trace: {error_trace}")
        
        # 返回错误响应
        return JSONResponse(
            content={
                "code": "A0002",
                "msg": f"服务器错误: {error_msg}",
                "data": {}
            }
        )

# 营销组分页查询接口
@app.post("/ces/group/list/page", response_model=GroupPageResponse)
async def group_list_page(request: Request, db: Session = Depends(get_db)):
    """
    营销组分页查询接口，支持按租户ID、公司ID、营销组名称筛选和分页
    
    请求示例:
    {
        "companyId": 0,  // 局点id
        "name": "",      // 营销组名称
        "pageNo": 1,
        "pageSize": 10,
        "tenantId": 0    // 运营商id
    }
    
    - 如果companyId为0，查询所有公司的营销组
    - 如果tenantId为0，查询所有租户的营销组
    - 支持按营销组名称模糊查询
    - 支持分页功能
    """
    try:
        # 读取请求体
        body_bytes = await request.body()
        
        # 解析JSON请求
        if not body_bytes:
            company_id = 0
            group_name = ""
            page_no = 1
            page_size = 10
            tenant_id = 0
        else:
            import json
            try:
                body = json.loads(body_bytes)
                company_id = body.get("companyId", 0)
                group_name = body.get("name", "")
                page_no = body.get("pageNo", 1)
                page_size = body.get("pageSize", 10)
                tenant_id = body.get("tenantId", 0)
            except json.JSONDecodeError:
                company_id = 0
                group_name = ""
                page_no = 1
                page_size = 10
                tenant_id = 0
        
        # 创建基础查询，包含营销组和关联的公司、租户信息
        query = db.query(
            models.Group.id,
            models.Group.name.label("group_name"),
            models.Group.description,
            models.Group.company_id,
            models.Group.create_time,
            models.Group.update_time,
            models.Group.operator_name,
            models.Company.name.label("company_name"),
            models.Company.tenant_id,
            models.Tenant.name.label("tenant_name")
        ).join(
            models.Company, models.Group.company_id == models.Company.id
        ).join(
            models.Tenant, models.Company.tenant_id == models.Tenant.id
        )
        
        # 应用过滤条件：营销组名称模糊查询
        if group_name:
            query = query.filter(models.Group.name.like(f'%{group_name}%'))
        
        # 应用过滤条件：公司ID
        if company_id and company_id != 0:
            query = query.filter(models.Group.company_id == company_id)
        
        # 应用过滤条件：租户ID
        if tenant_id and tenant_id != 0:
            query = query.filter(models.Company.tenant_id == tenant_id)
        
        # 获取总记录数，创建一个复制的查询以计算总数
        total_query = query
        total_records = total_query.count()
        
        # 分页处理
        if page_no > 0 and page_size > 0:
            query = query.offset((page_no - 1) * page_size).limit(page_size)
            current_page = page_no
            page_size = page_size
            total_pages = math.ceil(total_records / page_size) if page_size > 0 else 1
        else:
            # 不分页，返回所有记录
            current_page = 1
            page_size = total_records
            total_pages = 1
        
        # 执行查询
        group_results = query.all()
        
        # 构建响应数据
        records = []
        
        for group in group_results:
            # 格式化日期时间
            create_time = group.create_time.strftime("%Y-%m-%d %H:%M:%S") if group.create_time else None
            update_time = group.update_time.strftime("%Y-%m-%d %H:%M:%S") if group.update_time else None
            
            records.append({
                "id": group.id,
                "groupName": group.group_name,
                "description": group.description,
                "companyId": group.company_id,
                "companyName": group.company_name,
                "tenantId": group.tenant_id,
                "tenantName": group.tenant_name,
                "createTime": create_time,
                "updateTime": update_time,
                "operatorName": group.operator_name
            })
        
        # 返回成功响应
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": {
                    "records": records,
                    "total": total_records,
                    "size": page_size,
                    "current": current_page,
                    "pages": total_pages
                }
            }
        )
        
    except Exception as e:
        # 捕获所有异常并返回友好的错误信息
        import traceback
        error_detail = traceback.format_exc()
        print(f"Error in group_list_page: {str(e)}\n{error_detail}")
        
        return JSONResponse(
            status_code=200,  # 使用200而不是500，客户端更友好
            content={
                "code": "A0500",
                "msg": f"服务器内部错误: {str(e)}",
                "data": {
                    "records": [],
                    "total": 0,
                    "size": page_size if 'page_size' in locals() else 10,
                    "current": page_no if 'page_no' in locals() else 1,
                    "pages": 0
                }
            }
        )

# 新增营销组接口
@app.post("/ces/group/add", response_model=GroupAddResponse)
async def group_add(request: Request, db: Session = Depends(get_db)):
    """
    新增营销组接口
    
    请求示例:
    {
        "companyId": 1,  // 局点id
        "description": "营销组描述",
        "name": "营销组名称"
    }
    """
    try:
        # 读取请求体
        body_bytes = await request.body()
        
        # 解析JSON
        if not body_bytes:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体不能为空",
                    "data": {}
                }
            )
            
        import json
        try:
            body = json.loads(body_bytes)
            company_id = body.get("companyId")
            name = body.get("name")
            description = body.get("description", "")
        except json.JSONDecodeError:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体格式错误",
                    "data": {}
                }
            )
        
        # 验证必填字段
        if company_id is None:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "局点ID不能为空",
                    "data": {}
                }
            )
            
        if not name:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "营销组名称不能为空",
                    "data": {}
                }
            )
        
        # 验证局点是否存在
        company = db.query(models.Company).filter(models.Company.id == company_id).first()
        if not company:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": f"局点ID {company_id} 不存在",
                    "data": {}
                }
            )
        
        # 查询关联的租户信息
        tenant = db.query(models.Tenant).filter(models.Tenant.id == company.tenant_id).first()
        
        # 创建新营销组
        current_time = datetime.now()
        new_group = models.Group(
            name=name,
            description=description,
            company_id=company_id,
            create_time=current_time,
            update_time=current_time,
            operator_name="管理员"  # 默认操作人
        )
        
        # 保存到数据库
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
        
        # 返回成功响应
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": {
                    "id": new_group.id,
                    "groupName": new_group.name,
                    "description": new_group.description,
                    "companyId": new_group.company_id,
                    "companyName": company.name,
                    "tenantId": company.tenant_id,
                    "tenantName": tenant.name if tenant else "未知租户",
                    "createTime": new_group.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "updateTime": new_group.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "operatorName": new_group.operator_name
                }
            }
        )
        
    except Exception as e:
        # 处理异常
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        # 记录错误日志
        print(f"Error in group_add: {error_msg}")
        print(f"Trace: {error_trace}")
        
        # 返回错误响应
        return JSONResponse(
            content={
                "code": "A0002",
                "msg": f"服务器错误: {error_msg}",
                "data": {}
            }
        )

# 修改营销组接口
@app.post("/ces/group/modify", response_model=GroupModifyResponse)
async def group_modify(request: Request, db: Session = Depends(get_db)):
    """
    修改营销组接口
    
    请求示例:
    {
        "id": 1,
        "companyId": 2,       // 可选
        "name": "新营销组名称", // 可选
        "description": "新描述" // 可选
    }
    """
    try:
        # 读取请求体
        body_bytes = await request.body()
        
        # 解析JSON
        if not body_bytes:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体不能为空",
                    "data": {}
                }
            )
            
        import json
        try:
            body = json.loads(body_bytes)
            group_id = body.get("id")
            company_id = body.get("companyId")
            name = body.get("name")
            description = body.get("description")
        except json.JSONDecodeError:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "请求体格式错误",
                    "data": {}
                }
            )
        
        # 验证必填字段
        if group_id is None:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": "营销组ID不能为空",
                    "data": {}
                }
            )
        
        # 查询要修改的营销组
        group = db.query(models.Group).filter(models.Group.id == group_id).first()
        if not group:
            return JSONResponse(
                content={
                    "code": "A0001", 
                    "msg": f"营销组ID {group_id} 不存在",
                    "data": {}
                }
            )
        
        # 准备修改后的数据 
        updated_company_id = group.company_id
        updated_name = group.name
        updated_description = group.description
        
        # 如果提供了新的公司ID，验证公司是否存在并更新
        if company_id is not None:
            company = db.query(models.Company).filter(models.Company.id == company_id).first()
            if not company:
                return JSONResponse(
                    content={
                        "code": "A0001", 
                        "msg": f"局点ID {company_id} 不存在",
                        "data": {}
                    }
                )
            updated_company_id = company_id
        
        # 如果提供了新的名称，检查并更新
        if name is not None:
            if not name.strip():  # 检查名称不能为空或只包含空格
                return JSONResponse(
                    content={
                        "code": "A0001", 
                        "msg": "营销组名称不能为空",
                        "data": {}
                    }
                )
            updated_name = name
        
        # 如果提供了新的描述，更新
        if description is not None:
            updated_description = description
        
        # 更新营销组信息
        group.company_id = updated_company_id
        group.name = updated_name
        group.description = updated_description
        group.update_time = datetime.now()  # 更新修改时间
        
        # 保存到数据库
        db.commit()
        db.refresh(group)
        
        # 获取更新后的关联信息
        company = db.query(models.Company).filter(models.Company.id == group.company_id).first()
        tenant = None
        if company:
            tenant = db.query(models.Tenant).filter(models.Tenant.id == company.tenant_id).first()
        
        # 返回成功响应
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": {
                    "id": group.id,
                    "groupName": group.name,
                    "description": group.description,
                    "companyId": group.company_id,
                    "companyName": company.name if company else "未知公司",
                    "tenantId": company.tenant_id if company else 0,
                    "tenantName": tenant.name if tenant else "未知租户",
                    "updateTime": group.update_time.strftime("%Y-%m-%d %H:%M:%S") if group.update_time else None,
                    "operatorName": group.operator_name
                }
            }
        )
        
    except Exception as e:
        # 处理异常
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        # 记录错误日志
        print(f"Error in group_modify: {error_msg}")
        print(f"Trace: {error_trace}")
        
        # 返回错误响应
        return JSONResponse(
            content={
                "code": "A0002",
                "msg": f"服务器错误: {error_msg}",
                "data": {}
            }
        )

# 删除营销组接口
@app.delete("/ces/group/delete", response_model=GroupDeleteResponse)
async def group_delete(id: int, db: Session = Depends(get_db)):
    """
    删除营销组接口
    
    示例：DELETE /ces/group/delete?id=1 删除ID为1的营销组
    """
    try:
        # 查询要删除的营销组
        group = db.query(models.Group).filter(models.Group.id == id).first()
        
        # 如果营销组不存在，返回错误
        if not group:
            return JSONResponse(
                content={
                    "code": "A0001",
                    "msg": f"营销组ID {id} 不存在",
                    "data": {}
                }
            )
        
        # 获取公司和租户信息，用于返回
        company = db.query(models.Company).filter(models.Company.id == group.company_id).first()
        tenant = None
        if company:
            tenant = db.query(models.Tenant).filter(models.Tenant.id == company.tenant_id).first()
            
        # 保存营销组信息用于返回
        group_info = {
            "id": group.id,
            "groupName": group.name,
            "description": group.description,
            "companyId": group.company_id,
            "companyName": company.name if company else "未知公司",
            "tenantId": company.tenant_id if company else 0,
            "tenantName": tenant.name if tenant else "未知租户"
        }
        
        # 删除营销组
        db.delete(group)
        db.commit()
        
        # 返回成功响应
        return JSONResponse(
            content={
                "code": "00000",
                "msg": "成功",
                "data": group_info
            }
        )
        
    except Exception as e:
        # 处理异常
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        
        # 记录错误日志
        print(f"Error in group_delete: {error_msg}")
        print(f"Trace: {error_trace}")
        
        # 返回错误响应
        return JSONResponse(
            content={
                "code": "A0002",
                "msg": f"服务器错误: {error_msg}",
                "data": {}
            }
        )

# 查询局点和营销组的树形结构接口
@app.get("/ces/group/company_group/tree", response_model=GroupTreeResponse)
async def company_group_tree(companyId: int, db: Session = Depends(get_db)):
    # 获取公司信息
    company = db.query(models.Company).filter(models.Company.id == companyId).first()
    
    if not company:
        return {
            "code": "1",
            "msg": f"公司ID {companyId} 不存在",
            "data": None
        }
    
    # 获取所有营销组
    groups = db.query(models.Group).filter(models.Group.company_id == companyId).all()
    
    group_list = []
    for group in groups:
        group_list.append({
            "id": group.id,
            "name": group.name
        })
    
    response_data = {
        "companyId": company.id,
        "companyName": company.name,
        "groups": group_list
    }
    
    return {
        "code": "0",
        "msg": "成功",
        "data": response_data
    }

# 角色相关接口
@app.post("/ces/role/list/page")
async def role_list_page(request: Request, db: Session = Depends(get_db)):
    try:
        # 获取请求参数
        request_data = await request.json()
        name = request_data.get("name", "")
        page_no = request_data.get("pageNo", 1)
        page_size = request_data.get("pageSize", 10)
        
        # 查询条件
        query = db.query(models.Role)
        
        # 如果提供了name参数，添加过滤条件
        if name:
            query = query.filter(models.Role.name.like(f"%{name}%"))
        
        # 计算总数
        total = query.count()
        
        # 分页
        roles = query.offset((page_no - 1) * page_size).limit(page_size).all()
        
        # 构建结果
        records = []
        for role in roles:
            create_time = role.create_time.strftime("%Y-%m-%d %H:%M:%S") if role.create_time else None
            update_time = role.update_time.strftime("%Y-%m-%d %H:%M:%S") if role.update_time else None
            
            records.append({
                "id": role.id,
                "name": role.name,
                "description": role.description,
                "createTime": create_time,
                "updateTime": update_time,
                "operatorName": role.operator_name
            })
        
        # 计算总页数
        pages = math.ceil(total / page_size) if page_size > 0 else 0
        
        response_data = {
            "records": records,
            "total": total,
            "size": page_size,
            "current": page_no,
            "pages": pages
        }
        
        return {
            "code": "00000",
            "msg": "成功",
            "data": response_data
        }
    except Exception as e:
        return {
            "code": "A0002",
            "msg": f"查询失败: {str(e)}",
            "data": {
                "records": [],
                "total": 0,
                "size": 0,
                "current": 0,
                "pages": 0
            }
        }

@app.get("/ces/role/list")
async def role_list(db: Session = Depends(get_db)):
    try:
        # 查询所有角色
        roles = db.query(models.Role).all()
        
        # 构建结果
        role_list = []
        for role in roles:
            role_list.append({
                "id": role.id,
                "name": role.name
            })
        
        return {
            "code": "00000",
            "msg": "成功",
            "data": role_list
        }
    except Exception as e:
        return {
            "code": "A0002",
            "msg": f"查询失败: {str(e)}",
            "data": []
        }

@app.post("/ces/role/add")
async def role_add(request: Request, db: Session = Depends(get_db)):
    try:
        # 获取请求参数
        request_data = await request.json()
        name = request_data.get("name", "")
        description = request_data.get("description", "")
        
        if not name:
            return {
                "code": "A0001",
                "msg": "角色名称不能为空",
                "data": {}
            }
        
        # 检查角色名称是否已存在
        existing_role = db.query(models.Role).filter(models.Role.name == name).first()
        if existing_role:
            return {
                "code": "A0001",
                "msg": f"角色名称 '{name}' 已存在",
                "data": {}
            }
        
        # 创建新角色
        new_role = models.Role(
            name=name,
            description=description
        )
        
        db.add(new_role)
        db.commit()
        
        return {
            "code": "00000",
            "msg": "添加成功",
            "data": {}
        }
    except Exception as e:
        db.rollback()
        return {
            "code": "A0002",
            "msg": f"添加失败: {str(e)}",
            "data": {}
        }

@app.post("/ces/role/modify")
async def role_modify(request: Request, db: Session = Depends(get_db)):
    try:
        # 获取请求参数
        request_data = await request.json()
        role_id = request_data.get("id")
        name = request_data.get("name")
        description = request_data.get("description")
        
        if not role_id:
            return {
                "code": "A0001",
                "msg": "角色ID不能为空",
                "data": {}
            }
        
        # 查询角色是否存在
        role = db.query(models.Role).filter(models.Role.id == role_id).first()
        if not role:
            return {
                "code": "A0001",
                "msg": f"角色ID {role_id} 不存在",
                "data": {}
            }
        
        # 如果提供了新的名称，检查是否与其他角色重名
        if name and name != role.name:
            existing_role = db.query(models.Role).filter(
                models.Role.name == name,
                models.Role.id != role_id
            ).first()
            
            if existing_role:
                return {
                    "code": "A0001",
                    "msg": f"角色名称 '{name}' 已存在",
                    "data": {}
                }
            
            role.name = name
        
        # 更新描述
        if description is not None:
            role.description = description
        
        # 更新修改时间
        role.update_time = datetime.now()
        
        db.commit()
        
        return {
            "code": "00000",
            "msg": "修改成功",
            "data": {}
        }
    except Exception as e:
        db.rollback()
        return {
            "code": "A0002",
            "msg": f"修改失败: {str(e)}",
            "data": {}
        }

@app.delete("/ces/role/delete")
async def role_delete(id: int, db: Session = Depends(get_db)):
    try:
        # 查询角色是否存在
        role = db.query(models.Role).filter(models.Role.id == id).first()
        
        if not role:
            return {
                "code": "A0001",
                "msg": f"角色ID {id} 不存在",
                "data": {}
            }
        
        # 删除角色
        db.delete(role)
        db.commit()
        
        return {
            "code": "00000",
            "msg": "删除成功",
            "data": {}
        }
    except Exception as e:
        db.rollback()
        return {
            "code": "A0002",
            "msg": f"删除失败: {str(e)}",
            "data": {}
        }

# 标签相关接口
@app.post("/ces/label/list/page")
async def label_list_page(request: Request, db: Session = Depends(get_db)):
    try:
        # 获取请求参数
        request_data = await request.json()
        company_id = request_data.get("companyId", 0)
        name = request_data.get("name", "")
        page_no = request_data.get("pageNo", 1)
        page_size = request_data.get("pageSize", 10)
        label_type = request_data.get("type", 0)
        
        # 查询条件
        query = db.query(models.Label)
        
        # 如果提供了name参数，添加过滤条件
        if name:
            query = query.filter(models.Label.name.like(f"%{name}%"))
        
        # 如果提供了type参数，添加过滤条件
        if label_type and label_type > 0:
            query = query.filter(models.Label.type == label_type)
        
        # 如果提供了companyId参数，添加过滤条件
        label_ids = []
        if company_id and company_id > 0:
            # 查询与指定局点关联的标签ID
            label_companies = db.query(models.LabelCompany).filter(
                models.LabelCompany.company_id == company_id
            ).all()
            
            label_ids = [lc.label_id for lc in label_companies]
            if label_ids:
                query = query.filter(models.Label.id.in_(label_ids))
            else:
                # 如果没有与该局点关联的标签，返回空结果
                return {
                    "code": "00000",
                    "msg": "成功",
                    "data": {
                        "records": [],
                        "total": 0,
                        "size": page_size,
                        "current": page_no,
                        "pages": 0
                    }
                }
        
        # 计算总数
        total = query.count()
        
        # 分页
        labels = query.offset((page_no - 1) * page_size).limit(page_size).all()
        
        # 构建结果
        records = []
        for label in labels:
            # 查询标签关联的局点
            label_companies = db.query(models.LabelCompany).filter(
                models.LabelCompany.label_id == label.id
            ).all()
            
            company_ids = []
            company_names = []
            
            for lc in label_companies:
                company = db.query(models.Company).filter(
                    models.Company.id == lc.company_id
                ).first()
                
                if company:
                    company_ids.append(str(company.id))
                    company_names.append(company.name)
            
            # 类型名称
            type_value = LABEL_TYPE.get(label.type, "")
            
            records.append({
                "id": label.id,
                "name": label.name,
                "type": label.type,
                "typeValue": type_value,
                "companyIds": ",".join(company_ids),
                "companyNames": "，".join(company_names)  # 使用中文逗号
            })
        
        # 计算总页数
        pages = math.ceil(total / page_size) if page_size > 0 else 0
        
        response_data = {
            "records": records,
            "total": total,
            "size": page_size,
            "current": page_no,
            "pages": pages
        }
        
        return {
            "code": "00000",
            "msg": "成功",
            "data": response_data
        }
    except Exception as e:
        return {
            "code": "A0002",
            "msg": f"查询失败: {str(e)}",
            "data": {
                "records": [],
                "total": 0,
                "size": 0,
                "current": 0,
                "pages": 0
            }
        }

@app.post("/ces/label/add")
async def label_add(request: Request, db: Session = Depends(get_db)):
    try:
        # 获取请求参数
        request_data = await request.json()
        name = request_data.get("name", "")
        label_type = request_data.get("type", 0)
        
        if not name:
            return {
                "code": "A0001",
                "msg": "标签名称不能为空",
                "data": {}
            }
        
        if not label_type or label_type not in LABEL_TYPE:
            return {
                "code": "A0001",
                "msg": "标签类别无效",
                "data": {}
            }
        
        # 检查标签名称是否已存在
        existing_label = db.query(models.Label).filter(
            models.Label.name == name,
            models.Label.type == label_type
        ).first()
        
        if existing_label:
            return {
                "code": "A0001",
                "msg": f"同类别下标签名称 '{name}' 已存在",
                "data": {}
            }
        
        # 创建新标签
        new_label = models.Label(
            name=name,
            type=label_type
        )
        
        db.add(new_label)
        db.commit()
        db.refresh(new_label)
        
        return {
            "code": "00000",
            "msg": "添加成功",
            "data": {}
        }
    except Exception as e:
        db.rollback()
        return {
            "code": "A0002",
            "msg": f"添加失败: {str(e)}",
            "data": {}
        }

@app.post("/ces/label/modify")
async def label_modify(request: Request, db: Session = Depends(get_db)):
    try:
        # 获取请求参数
        request_data = await request.json()
        label_id = request_data.get("id")
        name = request_data.get("name")
        label_type = request_data.get("type")
        
        if not label_id:
            return {
                "code": "A0001",
                "msg": "标签ID不能为空",
                "data": {}
            }
        
        # 查询标签是否存在
        label = db.query(models.Label).filter(models.Label.id == label_id).first()
        if not label:
            return {
                "code": "A0001",
                "msg": f"标签ID {label_id} 不存在",
                "data": {}
            }
        
        # 如果提供了新的名称和类型，检查是否与其他标签重名
        if name is not None and label_type is not None and (name != label.name or label_type != label.type):
            existing_label = db.query(models.Label).filter(
                models.Label.name == name,
                models.Label.type == label_type,
                models.Label.id != label_id
            ).first()
            
            if existing_label:
                return {
                    "code": "A0001",
                    "msg": f"同类别下标签名称 '{name}' 已存在",
                    "data": {}
                }
        
        # 更新名称
        if name is not None:
            label.name = name
        
        # 更新类型
        if label_type is not None and label_type in LABEL_TYPE:
            label.type = label_type
        
        # 更新修改时间
        label.update_time = datetime.now()
        
        db.commit()
        
        return {
            "code": "00000",
            "msg": "修改成功",
            "data": {}
        }
    except Exception as e:
        db.rollback()
        return {
            "code": "A0002",
            "msg": f"修改失败: {str(e)}",
            "data": {}
        }

@app.delete("/ces/label/delete")
async def label_delete(id: int, db: Session = Depends(get_db)):
    try:
        # 查询标签是否存在
        label = db.query(models.Label).filter(models.Label.id == id).first()
        
        if not label:
            return {
                "code": "A0001",
                "msg": f"标签ID {id} 不存在",
                "data": {}
            }
        
        # 删除标签关联的局点
        db.query(models.LabelCompany).filter(
            models.LabelCompany.label_id == id
        ).delete()
        
        # 删除标签
        db.delete(label)
        db.commit()
        
        return {
            "code": "00000",
            "msg": "删除成功",
            "data": {}
        }
    except Exception as e:
        db.rollback()
        return {
            "code": "A0002",
            "msg": f"删除失败: {str(e)}",
            "data": {}
        }

@app.post("/ces/label/configure/label_company")
async def label_configure_company(request: Request, db: Session = Depends(get_db)):
    try:
        # 获取请求参数
        request_data = await request.json()
        label_id = request_data.get("id")
        company_list = request_data.get("companyList", [])
        
        if not label_id:
            return {
                "code": "A0001",
                "msg": "标签ID不能为空",
                "data": {}
            }
        
        # 查询标签是否存在
        label = db.query(models.Label).filter(models.Label.id == label_id).first()
        if not label:
            return {
                "code": "A0001",
                "msg": f"标签ID {label_id} 不存在",
                "data": {}
            }
        
        # 删除标签之前的关联局点
        db.query(models.LabelCompany).filter(
            models.LabelCompany.label_id == label_id
        ).delete()
        
        # 添加新的关联局点
        if company_list:
            for company_id in company_list:
                # 检查局点是否存在
                company = db.query(models.Company).filter(
                    models.Company.id == company_id
                ).first()
                
                if company:
                    # 创建新的关联关系
                    new_label_company = models.LabelCompany(
                        label_id=label_id,
                        company_id=company_id
                    )
                    
                    db.add(new_label_company)
        
        db.commit()
        
        return {
            "code": "00000",
            "msg": "配置成功",
            "data": {}
        }
    except Exception as e:
        db.rollback()
        return {
            "code": "A0002",
            "msg": f"配置失败: {str(e)}",
            "data": {}
        }

# 账号管理相关模型
class AccountItem(BaseModel):
    id: int
    tenantId: int
    tenantName: str
    companyId: int
    companyName: str
    username: str
    realName: str
    roleId: int
    roleName: str
    marketingGroups: List[int] = []
    marketingGroupNames: str
    enabled: int
    expireDate: Optional[str] = None
    expired: int
    creator: str
    createTime: Optional[str] = None
    updateTime: Optional[str] = None

class AccountPageData(BaseModel):
    records: List[AccountItem]
    total: int
    size: int
    current: int
    pages: int

class AccountPageResponse(BaseModel):
    code: str
    msg: str
    data: AccountPageData

class AccountPageRequest(BaseModel):
    tenantId: Optional[int] = None
    companyId: Optional[int] = None
    marketingGroups: Optional[List[int]] = None
    username: Optional[str] = ""
    realName: Optional[str] = ""
    enabled: Optional[int] = None
    expired: Optional[int] = None
    pageNo: Optional[int] = 1
    pageSize: Optional[int] = 10

class AccountAddRequest(BaseModel):
    tenantId: int
    companyId: int
    username: str
    realName: str
    password: str
    roleId: int
    marketingGroups: List[int] = []
    enabled: int = 1
    expireDate: Optional[str] = None

class AccountAddResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

class AccountModifyRequest(BaseModel):
    id: int
    tenantId: Optional[int] = None
    companyId: Optional[int] = None
    username: Optional[str] = None
    realName: Optional[str] = None
    password: Optional[str] = None
    roleId: Optional[int] = None
    marketingGroups: Optional[List[int]] = None
    enabled: Optional[int] = None
    expireDate: Optional[str] = None

class AccountModifyResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

class AccountDeleteResponse(BaseModel):
    code: str
    msg: str
    data: Optional[Dict] = {}

# 常量定义
ENABLED_STATUS = {
    1: "启用",
    2: "禁用"
}

EXPIRED_STATUS = {
    1: "已到期",
    2: "未到期"
}

# 账号管理相关API
@app.post("/ces/account/list/page")
async def account_list_page(request: Request, db: Session = Depends(get_db)):
    try:
        # 获取请求参数
        request_data = await request.json()
        tenant_id = request_data.get("tenantId")
        company_id = request_data.get("companyId")
        marketing_groups = request_data.get("marketingGroups", [])
        username = request_data.get("username", "")
        real_name = request_data.get("realName", "")
        enabled = request_data.get("enabled")
        expired = request_data.get("expired")
        page_no = request_data.get("pageNo", 1)
        page_size = request_data.get("pageSize", 10)
        
        # 查询条件
        query = db.query(models.UserAccount)
        
        # 添加过滤条件
        if tenant_id is not None:
            query = query.filter(models.UserAccount.tenant_id == tenant_id)
        
        if company_id is not None:
            query = query.filter(models.UserAccount.company_id == company_id)
        
        if username:
            query = query.filter(models.UserAccount.account.like(f"%{username}%"))
        
        if real_name:
            query = query.filter(models.UserAccount.name.like(f"%{real_name}%"))
        
        # 处理是否启用参数 (处理布尔值或整数)
        if enabled is not None:
            if isinstance(enabled, bool):
                query = query.filter(models.UserAccount.is_enabled == (1 if enabled else 0))
            else:
                query = query.filter(models.UserAccount.is_enabled == (1 if enabled == 1 else 0))
        
        # 处理是否到期参数 (处理布尔值或整数)
        if expired is not None:
            current_time = datetime.now()
            if isinstance(expired, bool):
                if expired:  # 已到期
                    query = query.filter(models.UserAccount.expire_date < current_time)
                else:  # 未到期
                    query = query.filter(
                        or_(
                            models.UserAccount.expire_date >= current_time,
                            models.UserAccount.expire_date == None
                        )
                    )
            else:
                if expired == 1:  # 已到期
                    query = query.filter(models.UserAccount.expire_date < current_time)
                elif expired == 2:  # 未到期
                    query = query.filter(
                        or_(
                            models.UserAccount.expire_date >= current_time,
                            models.UserAccount.expire_date == None
                        )
                    )
        
        # 如果提供了营销组ID，添加过滤条件 (使用关联表查询)
        if marketing_groups and len(marketing_groups) > 0:
            # 使用子查询获取与指定营销组关联的账号ID
            account_ids = db.query(models.AccountGroup.account_id).filter(
                models.AccountGroup.group_id.in_(marketing_groups)
            ).distinct().all()
            
            account_ids = [item[0] for item in account_ids]
            
            if account_ids:
                query = query.filter(models.UserAccount.id.in_(account_ids))
            else:
                # 没有找到相关账号，返回空结果
                return {
                    "code": "00000",
                    "msg": "成功",
                    "data": {
                        "records": [],
                        "total": 0,
                        "size": page_size,
                        "current": page_no,
                        "pages": 0
                    }
                }
        
        # 计算总数
        total = query.count()
        
        # 分页
        accounts = query.offset((page_no - 1) * page_size).limit(page_size).all()
        
        # 构建结果
        records = []
        for account in accounts:
            # 查询关联的租户
            tenant = db.query(models.Tenant).filter(
                models.Tenant.id == account.tenant_id
            ).first()
            
            # 查询关联的局点
            company = db.query(models.Company).filter(
                models.Company.id == account.company_id
            ).first()
            
            # 查询关联的角色
            role = db.query(models.Role).filter(
                models.Role.id == account.role_id
            ).first()
            
            # 查询关联的营销组 (从关联表获取全部营销组)
            group_ids = []
            group_names = []
            
            # 从关联表获取全部营销组
            account_groups = db.query(models.AccountGroup).filter(
                models.AccountGroup.account_id == account.id
            ).all()
            
            for account_group in account_groups:
                group = db.query(models.Group).filter(
                    models.Group.id == account_group.group_id
                ).first()
                
                if group:
                    group_ids.append(group.id)
                    group_names.append(group.name)
            
            # 判断是否过期
            expired_status = 0
            if account.expire_date:
                if account.expire_date < datetime.now():
                    expired_status = 1  # 已过期
                else:
                    expired_status = 2  # 未过期
            else:
                expired_status = 2  # 未过期
            
            records.append({
                "id": account.id,
                "tenantId": account.tenant_id,
                "tenantName": tenant.name if tenant else "",
                "companyId": account.company_id,
                "companyName": company.name if company else "",
                "username": account.account,
                "realName": account.name,
                "roleId": account.role_id,
                "roleName": role.name if role else "",
                "marketingGroups": group_ids,
                "marketingGroupNames": group_names,
                "enabled": account.is_enabled,
                "expireDate": account.expire_date.strftime("%Y-%m-%d %H:%M:%S") if account.expire_date else "",
                "expired": expired_status,
                "creator": account.creator,
                "createTime": account.create_time.strftime("%Y-%m-%d %H:%M:%S") if account.create_time else "",
                "updateTime": account.update_time.strftime("%Y-%m-%d %H:%M:%S") if account.update_time else ""
            })
        
        # 计算总页数
        pages = math.ceil(total / page_size) if page_size > 0 else 0
        
        response_data = {
            "records": records,
            "total": total,
            "size": page_size,
            "current": page_no,
            "pages": pages
        }
        
        return {
            "code": "00000",
            "msg": "成功",
            "data": response_data
        }
    except Exception as e:
        return {
            "code": "A0002",
            "msg": f"查询失败: {str(e)}",
            "data": {
                "records": [],
                "total": 0,
                "size": 0,
                "current": 0,
                "pages": 0
            }
        }

@app.post("/ces/account/add")
async def account_add(request: Request, db: Session = Depends(get_db)):
    try:
        # 获取请求参数
        request_data = await request.json()
        tenant_id = request_data.get("tenantId")
        company_id = request_data.get("companyId")
        username = request_data.get("username", "")
        real_name = request_data.get("realName", "")
        password = request_data.get("password", "123456")  # 使用默认密码123456
        role_id = request_data.get("roleId")
        marketing_groups = request_data.get("marketingGroups", [])
        enabled = request_data.get("enabled", 1)
        validity_type = request_data.get("validityType", "custom")
        expire_date_str = request_data.get("expireDate")
        
        if not username:
            return {
                "code": "A0001", 
                "msg": "用户账号不能为空",
                "data": {}
            }
        
        if not real_name:
            return {
                "code": "A0001",
                "msg": "用户名称不能为空",
                "data": {}
            }
        
        if not tenant_id:
            return {
                "code": "A0001",
                "msg": "运营商ID不能为空",
                "data": {}
            }
        
        if not company_id:
            return {
                "code": "A0001",
                "msg": "局点ID不能为空",
                "data": {}
            }
        
        # 检查用户账号是否已存在
        existing_account = db.query(models.UserAccount).filter(
            models.UserAccount.account == username
        ).first()
        
        if existing_account:
            return {
                "code": "A0001",
                "msg": f"用户账号 '{username}' 已存在",
                "data": {}
            }
        
        # 处理过期日期
        expire_date = None
        if expire_date_str:
            try:
                expire_date = datetime.strptime(expire_date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                try:
                    expire_date = datetime.strptime(expire_date_str, "%Y-%m-%d")
                except ValueError:
                    return {
                        "code": "A0001",
                        "msg": "过期日期格式错误，请使用YYYY-MM-DD HH:MM:SS或YYYY-MM-DD格式",
                        "data": {}
                    }
        
        # 提取主营销组ID（如果有多个，取第一个用于兼容旧字段）
        group_id = None
        if isinstance(marketing_groups, list) and len(marketing_groups) > 0:
            group_id = marketing_groups[0]
        
        # 创建新账号
        new_account = models.UserAccount(
            account=username,
            name=real_name,
            password=password,
            tenant_id=tenant_id,
            company_id=company_id,
            role_id=role_id if role_id else 1,  # 如果未提供角色ID，使用默认值1
            group_id=group_id,  # 保留兼容旧代码，只保存第一个营销组ID
            is_enabled=enabled,
            expire_date=expire_date
        )
        
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        
        # 创建账号-营销组关联
        if isinstance(marketing_groups, list) and marketing_groups:
            for group_id in marketing_groups:
                account_group = models.AccountGroup(
                    account_id=new_account.id,
                    group_id=group_id
                )
                db.add(account_group)
            
            db.commit()
        
        return {
            "code": "00000",
            "msg": "添加成功",
            "data": {}
        }
    except Exception as e:
        db.rollback()
        return {
            "code": "A0002",
            "msg": f"添加失败: {str(e)}",
            "data": {}
        }

@app.post("/ces/account/modify")
async def account_modify(request: Request, db: Session = Depends(get_db)):
    try:
        # 获取请求参数
        request_data = await request.json()
        account_id = request_data.get("id")
        tenant_id = request_data.get("tenantId")
        company_id = request_data.get("companyId")
        username = request_data.get("username")
        real_name = request_data.get("realName")
        password = request_data.get("password")
        role_id = request_data.get("roleId")
        marketing_groups = request_data.get("marketingGroups")
        enabled = request_data.get("enabled")
        validity_type = request_data.get("validityType")
        expire_date_str = request_data.get("expireDate")
        
        if not account_id:
            return {
                "code": "A0001",
                "msg": "账号ID不能为空",
                "data": {}
            }
        
        # 查询账号是否存在
        account = db.query(models.UserAccount).filter(models.UserAccount.id == account_id).first()
        if not account:
            return {
                "code": "A0001",
                "msg": f"账号ID {account_id} 不存在",
                "data": {}
            }
        
        # 如果提供了新的用户账号，检查是否与其他账号重名
        if username is not None and username != account.account:
            existing_account = db.query(models.UserAccount).filter(
                models.UserAccount.account == username,
                models.UserAccount.id != account_id
            ).first()
            
            if existing_account:
                return {
                    "code": "A0001",
                    "msg": f"用户账号 '{username}' 已存在",
                    "data": {}
                }
        
        # 更新账号信息
        if username is not None:
            account.account = username
        
        if real_name is not None:
            account.name = real_name
        
        if password is not None:
            account.password = password  # 实际应用中应该加密存储
        
        if tenant_id is not None:
            account.tenant_id = tenant_id
        
        if company_id is not None:
            account.company_id = company_id
        
        if role_id is not None:
            account.role_id = role_id
        
        # 处理营销组
        if marketing_groups is not None:
            # 更新主营销组字段（兼容性）
            if isinstance(marketing_groups, list) and len(marketing_groups) > 0:
                account.group_id = marketing_groups[0]  # 保留旧字段兼容性，只保存第一个
            else:
                account.group_id = None  # 如果是空列表，则清空营销组
            
            # 清除旧的账号-营销组关联
            db.query(models.AccountGroup).filter(
                models.AccountGroup.account_id == account_id
            ).delete()
            
            # 创建新的账号-营销组关联
            if isinstance(marketing_groups, list) and marketing_groups:
                for group_id in marketing_groups:
                    account_group = models.AccountGroup(
                        account_id=account_id,
                        group_id=group_id
                    )
                    db.add(account_group)
        
        if enabled is not None:
            account.is_enabled = enabled
        
        # 处理过期日期
        if expire_date_str is not None:
            if expire_date_str:
                try:
                    expire_date = datetime.strptime(expire_date_str, "%Y-%m-%d %H:%M:%S")
                    account.expire_date = expire_date
                except ValueError:
                    try:
                        expire_date = datetime.strptime(expire_date_str, "%Y-%m-%d")
                        account.expire_date = expire_date
                    except ValueError:
                        return {
                            "code": "A0001",
                            "msg": "过期日期格式错误，请使用YYYY-MM-DD HH:MM:SS或YYYY-MM-DD格式",
                            "data": {}
                        }
            else:
                account.expire_date = None
        
        # 更新修改时间
        account.update_time = datetime.now()
        
        db.commit()
        
        return {
            "code": "00000",
            "msg": "修改成功",
            "data": {}
        }
    except Exception as e:
        db.rollback()
        return {
            "code": "A0002",
            "msg": f"修改失败: {str(e)}",
            "data": {}
        }

@app.delete("/ces/account/delete")
async def account_delete(id: int, db: Session = Depends(get_db)):
    try:
        # 查询账号是否存在
        account = db.query(models.UserAccount).filter(models.UserAccount.id == id).first()
        
        if not account:
            return {
                "code": "A0001",
                "msg": f"账号ID {id} 不存在",
                "data": {}
            }
        
        # 删除账号-营销组关联
        db.query(models.AccountGroup).filter(models.AccountGroup.account_id == id).delete()
        
        # 删除账号
        db.delete(account)
        db.commit()
        
        return {
            "code": "00000",
            "msg": "删除成功",
            "data": {}
        }
    except Exception as e:
        db.rollback()
        return {
            "code": "A0002",
            "msg": f"删除失败: {str(e)}",
            "data": {}
        }

if __name__ == "__main__":
    import uvicorn
    # 确保数据库中有测试用户
    db = models.SessionLocal()
    try:
        # 检查是否已存在测试用户
        test_user = db.query(models.User).filter(models.User.username == "aaa").first()
        if not test_user:
            # 创建测试用户
            hashed_password = utils.get_password_hash("aaa")
            test_user = models.User(username="aaa", hashed_password=hashed_password)
            db.add(test_user)
            db.commit()
            
        # 添加示例运营商数据 - 使用更明确的名称
        tenants_data = [
            {"id": 1, "name": "中国联通"},
            {"id": 2, "name": "中国电信"},
            {"id": 3, "name": "中国移动"}
        ]
        
        # 更新或插入租户数据
        for tenant_data in tenants_data:
            tenant = db.query(models.Tenant).filter(models.Tenant.id == tenant_data["id"]).first()
            if tenant:
                # 更新租户名称
                tenant.name = tenant_data["name"]
            else:
                # 创建新租户
                tenant = models.Tenant(id=tenant_data["id"], name=tenant_data["name"])
                db.add(tenant)
        
        # 删除id=7的测试租户（如果存在）
        test_tenant = db.query(models.Tenant).filter(models.Tenant.id == 7).first()
        if test_tenant:
            db.delete(test_tenant)
        
        db.commit()
        
        # 删除现有公司数据
        db.query(models.Company).delete()
        db.commit()
        
        # 添加测试公司数据 - 名称更加明确区分
        test_companies = [
            # 联通公司
            {"id": 1, "name": "联通-北京分公司", "tenant_id": 1},
            {"id": 2, "name": "联通-上海分公司", "tenant_id": 1},
            {"id": 3, "name": "联通-广州分公司", "tenant_id": 1},
            
            # 电信公司
            {"id": 4, "name": "电信-北京分公司", "tenant_id": 2},
            {"id": 5, "name": "电信-上海分公司", "tenant_id": 2},
            {"id": 6, "name": "电信-广州分公司", "tenant_id": 2},
            
            # 移动公司
            {"id": 7, "name": "移动-北京分公司", "tenant_id": 3},
            {"id": 8, "name": "移动-上海分公司", "tenant_id": 3},
            {"id": 9, "name": "移动-广州分公司", "tenant_id": 3}
        ]
        
        for company_data in test_companies:
            company = models.Company(
                id=company_data["id"],
                name=company_data["name"],
                tenant_id=company_data["tenant_id"]
            )
            db.add(company)
        
        db.commit()
        companies = db.query(models.Company).all()
        
        # 清空现有网格数据
        db.query(models.Grid).delete()
        db.commit()
        
        # 区域数据 - 为每个城市设置更多的区域
        city_areas = {
            "北京": ["朝阳区", "海淀区", "东城区", "西城区", "丰台区", "石景山区", "通州区", "昌平区", "大兴区", "顺义区"],
            "上海": ["浦东新区", "静安区", "黄浦区", "徐汇区", "长宁区", "虹口区", "普陀区", "杨浦区", "闵行区", "宝山区"],
            "广州": ["天河区", "越秀区", "海珠区", "白云区", "荔湾区", "番禺区", "花都区", "黄埔区", "南沙区", "增城区"]
        }
        
        # 企业客户类型 - 为不同区域增加企业客户分类
        business_types = ["政府", "金融", "教育", "医疗", "商业"]
        
        # 添加测试网格数据 - 使用更丰富的命名
        grid_id = 1
        all_grids = []
        
        for company in companies:
            # 确定城市和运营商
            if "北京" in company.name:
                city = "北京"
                areas = city_areas["北京"]
            elif "上海" in company.name:
                city = "上海"
                areas = city_areas["上海"]
            elif "广州" in company.name:
                city = "广州"
                areas = city_areas["广州"]
                
            if "联通" in company.name:
                operator = "联通"
            elif "电信" in company.name:
                operator = "电信"
            elif "移动" in company.name:
                operator = "移动"
            else:
                operator = ""
            
            # 为每个区域创建普通网格
            for area in areas:
                grid_name = f"{operator}-{city}{area}网格"
                all_grids.append(models.Grid(id=grid_id, name=grid_name, company_id=company.id))
                grid_id += 1
            
            # 为前3个区域额外创建企业客户网格
            for area in areas[:3]:
                for business_type in business_types:
                    grid_name = f"{operator}-{city}{area}{business_type}客户网格"
                    all_grids.append(models.Grid(id=grid_id, name=grid_name, company_id=company.id))
                    grid_id += 1
        
        # 一次性批量添加所有网格
        db.add_all(all_grids)
        db.commit()
        
        # 统计数据
        total_grids = db.query(models.Grid).count()
        print(f"已添加测试数据: {len(tenants_data)}个运营商, {len(test_companies)}个局点, {total_grids}个网格")
        
        # 添加小区测试数据
        # 首先获取所有网格
        grids = db.query(models.Grid).all()
        
        # 为每个网格添加3-5个小区
        community_names = [
            "和平小区", "幸福家园", "阳光花园", "翠竹苑", "金色家园", 
            "未来城", "绿洲花园", "碧水云天", "紫荆苑", "蓝山小区",
            "梦想家园", "康乐居", "汇景苑", "华府名邸", "锦绣园",
            "御景华庭", "丽景花园", "凤凰城", "水岸新都", "江南新苑",
            "星河湾", "帝景豪园", "珠江花园", "山水名苑", "玫瑰园",
            "香榭丽舍", "半岛华府", "翡翠城", "龙湖花园", "万科城"
        ]
        
        for grid in grids:
            # 随机选择3-5个不重复的小区名
            num_communities = random.randint(3, 5)
            selected_names = random.sample(community_names, num_communities)
            
            # 为网格添加小区
            for name in selected_names:
                # 添加网格名称前缀，避免小区名称重复
                grid_prefix = grid.name.split('-')[0]  # 获取运营商名称作为前缀
                full_name = f"{grid_prefix}-{name}"
                
                # 创建小区
                community = models.Community(
                    name=full_name,
                    grid_id=grid.id,
                    create_time=datetime.now() - timedelta(days=random.randint(0, 365)),
                    update_time=datetime.now() - timedelta(days=random.randint(0, 30)),
                    operator_name=random.choice(["管理员", "操作员", "超级管理员", "系统"])
                )
                db.add(community)
        
        db.commit()
        
        print("数据初始化完成!")
    finally:
        db.close()
    
    # 确保使用8080端口
    print("正在启动服务器，端口：8080...")
    uvicorn.run(app, host="0.0.0.0", port=8080) 