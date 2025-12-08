# Backend 代码规范文档

## 概述

本项目后端采用 **Python 3.10+**，架构设计基于 **六边形架构（Hexagonal Architecture）**，也称为 **端口与适配器架构（Ports and Adapters）**。该架构的核心思想是将业务逻辑与外部依赖隔离，使系统更易于测试、维护和扩展。

依赖管理采用 **依赖注入（Dependency Injection, DI）** 模式，确保模块之间的松耦合。

---

## 架构原则

### 核心原则

1. **依赖倒置原则（DIP）**：高层模块不依赖低层模块，两者都依赖于抽象
2. **单一职责原则（SRP）**：每个模块只负责一个功能领域
3. **接口隔离原则（ISP）**：客户端不应该依赖它不需要的接口
4. **开闭原则（OCP）**：对扩展开放，对修改关闭

### 依赖方向

```
外部世界 → 适配器 → 端口（接口） → 领域核心 ← 端口（接口） ← 适配器 ← 外部世界
```

所有依赖指向领域核心，领域核心不依赖任何外部实现。

---

## 目录结构

```
backend/
├── src/
│   ├── domain/                      # 领域层 - 业务核心（纯 Python，无外部依赖）
│   │   ├── __init__.py
│   │   ├── entities.py              # 领域实体
│   │   ├── value_objects.py         # 值对象
│   │   ├── events.py                # 领域事件
│   │   ├── exceptions.py            # 领域异常
│   │   └── services.py              # 领域服务
│   │
│   ├── application/                 # 应用层 - 用例编排
│   │   ├── __init__.py
│   │   ├── ports.py                 # 端口定义（入站 + 出站接口）
│   │   ├── services.py              # 应用服务（用例实现）
│   │   ├── dto.py                   # 数据传输对象
│   │   └── mappers.py               # 对象映射器
│   │
│   ├── infrastructure/              # 基础设施层 - 技术实现
│   │   ├── __init__.py
│   │   ├── api/                     # HTTP API 适配器
│   │   │   ├── __init__.py
│   │   │   ├── routes.py            # 路由定义
│   │   │   ├── middlewares.py       # 中间件
│   │   │   └── dependencies.py      # FastAPI 依赖注入
│   │   ├── persistence/             # 持久化适配器
│   │   │   ├── __init__.py
│   │   │   ├── models.py            # ORM 模型
│   │   │   ├── repositories.py      # 仓储实现
│   │   │   └── migrations/          # 数据库迁移
│   │   ├── external/                # 外部服务适配器
│   │   │   ├── __init__.py
│   │   │   ├── cache.py             # 缓存（Redis）
│   │   │   ├── messaging.py         # 消息队列
│   │   │   └── storage.py           # 文件存储
│   │   └── config.py                # 配置管理
│   │
│   ├── shared/                      # 共享模块
│   │   ├── __init__.py
│   │   ├── utils.py                 # 工具函数
│   │   └── constants.py             # 常量定义
│   │
│   └── main.py                      # 应用入口
│
├── tests/                           # 测试目录
│   ├── unit/                        # 单元测试
│   ├── integration/                 # 集成测试
│   └── conftest.py                  # pytest 配置
│
├── .env.example
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## 各层职责说明

### 1. 领域层（Domain Layer）

**职责**：封装核心业务逻辑，不依赖任何外部框架或技术实现。

| 组件 | 职责 | 规范 |
|------|------|------|
| Entities | 具有唯一标识的业务对象 | 必须包含业务行为，不仅是数据容器 |
| Value Objects | 无标识的不可变对象 | 通过值相等性比较，必须是不可变的（使用 `@dataclass(frozen=True)`） |
| Aggregates | 一组相关对象的集合 | 有明确的边界和聚合根 |
| Domain Events | 领域中发生的事件 | 使用过去时命名，如 `UserCreatedEvent` |
| Domain Services | 不属于单个实体的业务逻辑 | 无状态，纯业务操作 |
| Domain Exceptions | 领域特定的异常 | 继承自基础 `DomainException` |

### 2. 应用层（Application Layer）

**职责**：编排用例，协调领域对象完成业务流程。

| 组件 | 职责 | 规范 |
|------|------|------|
| Inbound Ports | 定义应用对外提供的服务接口 | 使用 `ABC`（抽象基类）或 `Protocol` 定义 |
| Outbound Ports | 定义应用依赖的外部服务接口 | 使用 `ABC`（抽象基类）或 `Protocol` 定义 |
| Application Services | 实现用例逻辑 | 薄层，主要负责编排 |
| DTOs | 跨层数据传输 | 使用 `Pydantic` 或 `dataclass`，无业务逻辑 |
| Mappers | 对象转换 | 领域对象与DTO之间的转换 |

### 3. 基础设施层（Infrastructure Layer）

**职责**：提供技术实现，包括数据库、缓存、消息队列等。

| 组件 | 职责 | 规范 |
|------|------|------|
| Inbound Adapters | 接收外部请求 | 实现入站端口，如 FastAPI Router |
| Outbound Adapters | 与外部系统交互 | 实现出站端口，如 Repository |
| Config | 配置管理 | 使用 Pydantic Settings 管理环境配置 |
| DI Container | 依赖注入容器 | 管理对象生命周期和依赖关系 |

---

## 依赖注入规范

### 基本原则

1. **接口优先**：所有依赖都通过接口（端口）注入，不直接依赖具体实现
2. **构造函数注入**：优先使用构造函数注入，避免属性注入
3. **单一职责**：每个注入的依赖应该有明确的职责
4. **生命周期管理**：明确定义每个依赖的生命周期（Singleton、Scoped、Transient）

### 端口定义示例

```python
# application/ports.py
from abc import ABC, abstractmethod
from typing import Protocol, Optional, Any
from domain.entities import User


# ============ 入站端口（驱动端口）============

class IUserService(ABC):
    """用户服务端口"""
    
    @abstractmethod
    async def create_user(self, dto: "CreateUserDto") -> "UserResponseDto":
        pass
    
    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Optional["UserResponseDto"]:
        pass


# ============ 出站端口（被驱动端口）============

class IUserRepository(ABC):
    """用户仓储端口"""
    
    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def save(self, user: User) -> None:
        pass


class ICachePort(Protocol):
    """缓存端口（使用 Protocol 实现结构子类型）"""
    
    async def get(self, key: str) -> Optional[Any]: ...
    async def set(self, key: str, value: Any, ttl: int = 3600) -> None: ...
    async def delete(self, key: str) -> None: ...
```

### 应用服务示例

```python
# application/services.py
from dataclasses import dataclass
from typing import Optional

from application.ports import IUserService, IUserRepository
from application.dto import CreateUserDto, UserResponseDto
from application.mappers import UserMapper
from domain.entities import User
from domain.exceptions import UserAlreadyExistsException


@dataclass
class UserService(IUserService):
    """用户应用服务"""
    
    user_repository: IUserRepository
    
    async def create_user(self, dto: CreateUserDto) -> UserResponseDto:
        """创建用户用例"""
        existing_user = await self.user_repository.find_by_email(dto.email)
        if existing_user:
            raise UserAlreadyExistsException(dto.email)
        
        user = User.create(email=dto.email, name=dto.name, password=dto.password)
        await self.user_repository.save(user)
        
        return UserMapper.to_response_dto(user)
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserResponseDto]:
        """根据ID获取用户"""
        user = await self.user_repository.find_by_id(user_id)
        return UserMapper.to_response_dto(user) if user else None
```

### 依赖注入示例（FastAPI Depends）

```python
# infrastructure/api/dependencies.py
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from application.ports import IUserRepository
from application.services import UserService
from infrastructure.persistence.repositories import UserRepository
from infrastructure.config import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_user_repository(
    settings: Annotated[Settings, Depends(get_settings)]
) -> IUserRepository:
    return UserRepository(db_url=settings.database_url)


def get_user_service(
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)]
) -> UserService:
    return UserService(user_repository=user_repository)


# 类型别名
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
```

### 路由定义示例

```python
# infrastructure/api/routes.py
from fastapi import APIRouter, HTTPException, status

from application.dto import CreateUserDto, UserResponseDto
from infrastructure.api.dependencies import UserServiceDep

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponseDto, status_code=status.HTTP_201_CREATED)
async def create_user(dto: CreateUserDto, user_service: UserServiceDep):
    """创建用户"""
    return await user_service.create_user(dto)


@router.get("/{user_id}", response_model=UserResponseDto)
async def get_user(user_id: str, user_service: UserServiceDep):
    """获取用户详情"""
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
```

### 生命周期定义

| 生命周期 | 说明 | Python 实现 | 适用场景 |
|----------|------|-------------|----------|
| Singleton | 全局单例 | `@lru_cache` / `providers.Singleton` | 无状态服务、配置、数据库连接池 |
| Scoped | 每个请求一个实例 | `providers.Resource` / 中间件管理 | 请求相关的服务、事务管理 |
| Transient | 每次注入新实例 | `providers.Factory` / 普通函数 | 轻量级、无状态的临时对象 |

---

## 命名规范

### 文件命名

Python 使用 **snake_case** 命名文件：

| 类型 | 格式 | 示例 |
|------|------|------|
| 模块文件 | `{name}.py` | `entities.py`, `services.py` |
| 测试文件 | `test_{name}.py` | `test_user_service.py` |
| 配置文件 | `{name}.py` | `config.py`, `settings.py` |

### 类/接口命名

| 类型 | 格式 | 示例 |
|------|------|------|
| 实体类 | PascalCase | `User`, `Order` |
| 值对象 | PascalCase | `Email`, `Money` |
| 端口接口 | I + PascalCase | `IUserRepository`, `IUserService` |
| 应用服务 | PascalCase + Service | `UserService` |
| 控制器 | 使用 router 变量 | `router = APIRouter()` |
| 仓储实现 | PascalCase + Repository | `UserRepository` |
| DTO | PascalCase + Dto | `CreateUserDto`, `UserResponseDto` |
| 领域事件 | PascalCase + Event | `UserCreatedEvent` |
| 异常 | PascalCase + Exception/Error | `UserNotFoundException` |

### 方法/函数命名

| 操作 | 前缀 | 示例 |
|------|------|------|
| 查询单个 | `find_`, `get_` | `find_by_id()`, `get_user()` |
| 查询多个 | `find_all_`, `list_` | `find_all_by_status()`, `list_users()` |
| 创建 | `create_`, `add_` | `create_user()`, `add_order()` |
| 更新 | `update_`, `modify_` | `update_user()`, `modify_order()` |
| 删除 | `delete_`, `remove_` | `delete_user()`, `remove_order()` |
| 检查 | `is_`, `has_`, `can_` | `is_active()`, `has_permission()` |
| 转换 | `to_`, `from_` | `to_dto()`, `from_entity()` |
| 异步方法 | 同上规则 | `async def find_by_id()` |

### 变量命名

| 类型 | 格式 | 示例 |
|------|------|------|
| 普通变量 | snake_case | `user_name`, `order_id` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT`, `DEFAULT_PAGE_SIZE` |
| 私有变量 | _snake_case | `_internal_cache` |
| 类型变量 | PascalCase | `T`, `UserType` |

---

## 代码组织规范

### 导入顺序

```python
# 1. 标准库
import os
from typing import Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

# 2. 第三方库
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

# 3. 领域层
from domain.entities import User
from domain.events import UserCreatedEvent

# 4. 应用层
from application.ports import IUserRepository
from application.dto import CreateUserDto

# 5. 基础设施层
from infrastructure.persistence.models import UserModel

# 6. 共享模块
from shared.utils import format_date

# 7. 相对路径导入（同一包内）
from .helpers import local_helper
```

### 模块导出

使用 `__init__.py` 统一导出：

```python
# domain/__init__.py
from .entities import User, Order
from .exceptions import DomainException, UserNotFoundException

__all__ = ["User", "Order", "DomainException", "UserNotFoundException"]
```

### 类型注解

使用 Python 3.10+ 的类型注解语法：

```python
# 使用新语法（Python 3.10+）
def find_users(status: str | None = None) -> list[User]:
    ...

# 使用 Optional 和 List（兼容旧版本）
from typing import Optional, List

def find_users(status: Optional[str] = None) -> List[User]:
    ...
```

### DTO 定义（使用 Pydantic）

```python
# application/dto.py
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


# ============ Request DTOs ============

class CreateUserDto(BaseModel):
    """创建用户请求"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)


class UpdateUserDto(BaseModel):
    """更新用户请求"""
    name: str | None = None
    email: EmailStr | None = None


# ============ Response DTOs ============

class UserResponseDto(BaseModel):
    """用户响应"""
    id: str
    email: str
    name: str
    created_at: datetime
    
    model_config = {"from_attributes": True}
```

### 领域实体定义

```python
# domain/entities.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class User:
    """用户领域实体"""
    id: str
    email: str
    name: str
    password_hash: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    @classmethod
    def create(cls, email: str, name: str, password: str) -> "User":
        """工厂方法：创建新用户"""
        from shared.utils import hash_password
        return cls(
            id=str(uuid.uuid4()),
            email=email,
            name=name,
            password_hash=hash_password(password),
            created_at=datetime.utcnow()
        )
    
    def update_name(self, new_name: str) -> None:
        """更新用户名称"""
        if not new_name or len(new_name) > 100:
            raise ValueError("Invalid name")
        self.name = new_name
        self.updated_at = datetime.utcnow()
```

### 值对象定义

```python
# domain/value_objects.py
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Email:
    """邮箱值对象（不可变）"""
    value: str
    
    def __post_init__(self):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.value):
            raise ValueError(f"Invalid email: {self.value}")


@dataclass(frozen=True)
class Money:
    """金额值对象"""
    amount: int  # 以分为单位
    currency: str = "CNY"
```

### 异常定义

```python
# domain/exceptions.py
class DomainException(Exception):
    """领域异常基类"""
    def __init__(self, message: str, code: str = "DOMAIN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class UserNotFoundException(DomainException):
    def __init__(self, user_id: str):
        super().__init__(f"User not found: {user_id}", "USER_NOT_FOUND")


class UserAlreadyExistsException(DomainException):
    def __init__(self, email: str):
        super().__init__(f"User already exists: {email}", "USER_ALREADY_EXISTS")
```

### 异常处理中间件

```python
# infrastructure/api/middlewares.py
from fastapi import Request
from fastapi.responses import JSONResponse
from domain.exceptions import DomainException, UserNotFoundException


async def domain_exception_handler(request: Request, exc: DomainException):
    """领域异常处理器"""
    status_code = 404 if isinstance(exc, UserNotFoundException) else 400
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": exc.code, "message": exc.message}}
    )
```

---

## 测试规范

### 测试分层

| 层级 | 目录 | 测试内容 | Mock 策略 |
|------|------|----------|-----------|
| 单元测试 | `tests/unit/` | 领域逻辑、应用服务 | Mock 所有外部依赖 |
| 集成测试 | `tests/integration/` | 适配器实现 | 使用真实数据库/缓存 |
| E2E测试 | `tests/e2e/` | 完整业务流程 | 最小化 Mock |

### 测试示例

```python
# tests/unit/test_user_service.py
import pytest
from unittest.mock import AsyncMock, MagicMock

from application.services import UserService
from application.dto import CreateUserDto
from domain.exceptions import UserAlreadyExistsException


class TestUserService:
    @pytest.fixture
    def mock_repo(self):
        return AsyncMock()
    
    @pytest.fixture
    def service(self, mock_repo):
        return UserService(user_repository=mock_repo)
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, service, mock_repo):
        """邮箱唯一时应成功创建用户"""
        dto = CreateUserDto(email="test@example.com", name="Test", password="password123")
        mock_repo.find_by_email.return_value = None
        
        result = await service.create_user(dto)
        
        assert result.email == dto.email
        mock_repo.save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_user_email_exists(self, service, mock_repo):
        """邮箱已存在时应抛出异常"""
        dto = CreateUserDto(email="exists@example.com", name="Test", password="password123")
        mock_repo.find_by_email.return_value = MagicMock()
        
        with pytest.raises(UserAlreadyExistsException):
            await service.create_user(dto)
```

### pytest 配置

```ini
# pyproject.toml
[tool.pytest.ini_options]
minversion = "7.0"
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

---

## 配置管理

### 使用 Pydantic Settings

```python
# infrastructure/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    
    # 应用
    app_name: str = "App Management Hub"
    debug: bool = False
    
    # 数据库
    database_url: str = "postgresql://localhost/app_db"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # JWT
    jwt_secret_key: str = "change-me"
    jwt_expire_minutes: int = 30


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

---

## 最佳实践

### Do ✅

- 保持领域层的纯净，不引入框架依赖
- 通过端口定义清晰的边界
- 使用依赖注入解耦组件
- 编写有意义的单元测试
- 遵循 SOLID 原则
- 使用类型注解提高代码可读性
- 使用 `async/await` 处理 I/O 操作
- 使用 Pydantic 进行数据验证
- 保持小而专注的函数和类
- 使用 `dataclass` 或 Pydantic 定义数据结构

### Don't ❌

- 在领域层直接使用 ORM 模型
- 在应用服务中处理 HTTP 相关逻辑
- 在控制器中编写业务逻辑
- 循环依赖
- 在领域层使用基础设施层的类型
- 跳过端口直接依赖具体实现
- 在测试中使用真实的外部服务
- 使用可变默认参数（如 `def func(items=[])`）
- 忽略异常或使用裸 `except:`

---

## 推荐工具链

| 用途 | 工具 | 说明 |
|------|------|------|
| Web 框架 | FastAPI | 高性能异步框架，自带 OpenAPI 文档 |
| ORM | SQLAlchemy 2.0 | 支持异步，类型安全 |
| 数据验证 | Pydantic v2 | 高性能数据验证和序列化 |
| 依赖注入 | dependency-injector / FastAPI Depends | 灵活的 DI 解决方案 |
| 测试 | pytest + pytest-asyncio | 强大的测试框架 |
| 代码格式化 | Black + isort | 统一代码风格 |
| 类型检查 | mypy / pyright | 静态类型检查 |
| Linter | Ruff | 快速的 Python linter |
| 包管理 | Poetry / PDM | 现代化依赖管理 |

---

## 参考资料

- [Hexagonal Architecture (Alistair Cockburn)](https://alistair.cockburn.us/hexagonal-architecture/)
- [Clean Architecture (Robert C. Martin)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design (Eric Evans)](https://domainlanguage.com/ddd/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/)
- [dependency-injector](https://python-dependency-injector.ets-labs.org/)
