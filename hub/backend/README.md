# App Management Backend

应用管理模块后端服务 - 管理 DIP 应用的全生命周期。

## 功能特性

- 创建应用
- 上传应用安装包（ZIP）
- 编辑应用元数据
- 更新应用包
- 发布 / 撤销发布
- 删除应用
- 浏览应用列表
- 浏览应用详情

## 技术栈

- **Python 3.10+**
- **FastAPI** - 高性能异步 Web 框架
- **SQLAlchemy 2.0** - ORM
- **MariaDB** - 数据库
- **Pydantic** - 数据验证

## 架构

项目采用六边形架构（Hexagonal Architecture）：

```
src/
├── domain/           # 领域层 - 业务核心
├── application/      # 应用层 - 用例编排
├── infrastructure/   # 基础设施层 - 技术实现
└── shared/           # 共享模块
```

## 快速开始

### 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖（可选）
pip install -r requirements-dev.txt
```

### 配置环境变量

复制环境变量模板并修改：

```bash
cp .env.example .env
```

### 运行服务

```bash
cd src
python main.py
```

服务启动后访问：
- API 文档：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc

## API 接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /dip/v1/apps/ | 创建应用 |
| GET | /dip/v1/apps/ | 浏览应用列表 |
| GET | /dip/v1/apps/{id} | 查看应用详情 |
| PUT | /dip/v1/apps/{id} | 编辑应用 |
| DELETE | /dip/v1/apps/{id} | 删除应用 |
| POST | /dip/v1/apps/{id}/packages/upload | 上传应用包 |
| POST | /dip/v1/apps/{id}/publish | 发布应用 |
| POST | /dip/v1/apps/{id}/unpublish | 撤销发布 |

## 运行测试

```bash
# 运行所有测试
pytest

# 运行并显示覆盖率
pytest --cov=src --cov-report=html

# 只运行单元测试
pytest tests/unit/

# 只运行集成测试
pytest tests/integration/
```

## 数据库

### 创建数据库

```sql
CREATE DATABASE app_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 表结构

详见设计文档中的数据库设计部分。

## 开发指南

### 代码风格

项目使用以下工具保持代码风格一致：

```bash
# 格式化代码
black src tests
isort src tests

# 检查代码
ruff check src tests

# 类型检查
mypy src
```

### 目录结构说明

- `domain/` - 领域实体、异常、事件（纯 Python，无外部依赖）
- `application/` - 端口定义、应用服务、DTO、映射器
- `infrastructure/` - API 路由、持久化、外部服务适配器
- `shared/` - 工具函数、常量
- `tests/` - 单元测试和集成测试

## License

MIT

