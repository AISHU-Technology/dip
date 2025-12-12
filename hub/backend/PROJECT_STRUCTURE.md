# DIP Hub 项目结构说明文档

## 项目概述

DIP Hub 是一个基于**六边形架构（端口-适配器架构）**设计的 Python Web 应用程序。该架构将核心业务逻辑与外部基础设施完全隔离，通过端口（Ports）定义抽象接口，由适配器（Adapters）提供具体实现。

## 技术栈

- **语言**: Python 3.10+
- **Web框架**: FastAPI
- **配置管理**: Pydantic Settings
- **服务器**: Uvicorn
- **架构模式**: 六边形架构（Hexagonal Architecture / Ports and Adapters）

## 目录结构

```
hub/backend/
├── src/                          # 源代码目录
│   ├── __init__.py               # 包初始化文件
│   ├── main.py                   # 应用入口点
│   ├── domains/                  # 领域层 - 核心业务模型
│   │   ├── __init__.py
│   │   └── health.py             # 健康检查领域模型
│   ├── ports/                    # 端口层 - 接口定义
│   │   ├── __init__.py
│   │   └── health_port.py        # 健康检查端口接口
│   ├── application/              # 应用层 - 业务用例
│   │   ├── __init__.py
│   │   └── health_service.py     # 健康检查应用服务
│   ├── adapters/                 # 适配器层 - 端口接口实现
│   │   ├── __init__.py
│   │   └── health_adapter.py     # 健康检查适配器
│   ├── infrastructure/           # 基础设施层 - 配置、日志等
│   │   ├── __init__.py
│   │   ├── container.py          # 依赖注入容器
│   │   ├── config/               # 配置模块
│   │   │   ├── __init__.py
│   │   │   └── settings.py       # 应用配置
│   │   └── logging/              # 日志模块
│   │       ├── __init__.py
│   │       └── logger.py         # 日志配置
│   └── routers/                  # 路由层 - API接口适配器
│       ├── __init__.py
│       ├── health_router.py      # 健康检查路由
│       └── schemas/              # API响应模型
│           ├── __init__.py
│           └── health.py         # 健康检查响应模型
├── tests/                        # 测试代码目录
│   ├── __init__.py
│   ├── conftest.py               # pytest配置
│   └── test_health.py            # 健康检查测试
├── requirements.txt              # Python依赖
├── Makefile                      # 构建命令
├── Dockerfile                    # Docker镜像构建
└── PROJECT_STRUCTURE.md          # 项目结构说明（本文档）
```

## 各层详细说明

### 1. 领域层 (src/domains/)

**职责**: 定义核心业务模型和业务逻辑，不依赖任何外部技术细节。

| 文件 | 说明 |
|------|------|
| `health.py` | 定义健康检查相关的领域模型，包括 `HealthStatus`、`ReadyStatus` 枚举以及 `HealthCheckResult`、`ReadyCheckResult` 数据类 |

**设计原则**:
- 纯Python代码，不依赖任何外部框架
- 定义业务概念和规则
- 可独立于基础设施进行单元测试

---

### 2. 端口层 (src/ports/)

**职责**: 定义抽象接口（端口），作为领域层与外部世界交互的契约。

| 文件 | 说明 |
|------|------|
| `health_port.py` | 定义 `HealthCheckPort` 抽象基类，声明 `check_health()`、`check_ready()`、`get_service_info()` 等方法 |

**设计原则**:
- 使用抽象基类（ABC）定义接口
- 只定义方法签名，不包含实现
- 遵循依赖倒置原则（DIP）

---

### 3. 应用层 (src/application/)

**职责**: 实现业务用例，编排领域操作，通过端口与外部交互。

| 文件 | 说明 |
|------|------|
| `health_service.py` | 健康检查应用服务，封装健康检查的业务用例，通过注入的端口实现与适配器的交互 |

**设计原则**:
- 依赖端口接口，不依赖具体实现
- 协调领域对象完成业务用例
- 接收适配器注入，实现依赖反转

---

### 4. 适配器层 (src/adapters/)

**职责**: 提供端口的具体实现，将外部技术细节转换为领域可理解的操作。

| 文件 | 说明 |
|------|------|
| `health_adapter.py` | 实现 `HealthCheckPort` 接口的具体适配器，提供健康检查的实际逻辑 |

**设计原则**:
- 实现端口定义的接口
- 处理所有技术细节（数据库、HTTP、消息队列等）
- 可替换，不影响核心业务逻辑

---

### 5. 基础设施层 (src/infrastructure/)

**职责**: 提供基础设施支持，包括配置管理、日志、依赖注入等。

#### 5.1 配置模块 (config/)

| 文件 | 说明 |
|------|------|
| `settings.py` | 使用 Pydantic Settings 管理应用配置，支持环境变量和 `.env` 文件配置 |

**配置项**:
- `DIP_HUB_HOST`: 服务监听地址（默认：0.0.0.0）
- `DIP_HUB_PORT`: 服务监听端口（默认：8000）
- `DIP_HUB_DEBUG`: 调试模式（默认：false）
- `DIP_HUB_LOG_LEVEL`: 日志级别（默认：INFO）

#### 5.2 日志模块 (logging/)

| 文件 | 说明 |
|------|------|
| `logger.py` | 日志配置和工厂方法 |

#### 5.3 依赖注入容器

| 文件 | 说明 |
|------|------|
| `container.py` | 依赖注入容器，负责组装适配器并注入到应用服务中 |

---

### 6. 路由层 (src/routers/)

**职责**: 作为输入适配器，处理HTTP请求并委托给应用层。

| 文件 | 说明 |
|------|------|
| `health_router.py` | FastAPI路由控制器，定义健康检查相关的HTTP端点 |
| `schemas/health.py` | Pydantic模型，定义API请求和响应的数据结构 |

**API端点**:
- `GET /api/internal/dip-hub/v1/health` - 健康检查
- `GET /api/internal/dip-hub/v1/ready` - 就绪检查
- `GET /api/internal/dip-hub/v1/info` - 服务信息

---

### 7. 入口点 (src/main.py)

**职责**: 应用程序入口，负责：
- 初始化配置
- 创建依赖注入容器
- 组装FastAPI应用
- 注册路由
- 启动Web服务

---

### 8. 测试目录 (tests/)

**职责**: 包含单元测试和集成测试。

| 文件 | 说明 |
|------|------|
| `conftest.py` | Pytest配置和共享fixtures |
| `test_health.py` | 健康检查相关测试 |

---

## 架构依赖关系图

```
┌─────────────────────────────────────────────────────────────────┐
│                        外部世界                                  │
│  (HTTP Clients, 数据库, 消息队列, 第三方服务...)                  │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     路由层 (routers/)                            │
│                    FastAPI 路由控制器                            │
│              (输入适配器 - Driving Adapter)                      │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    应用层 (application/)                         │
│                      应用服务/用例                                │
│                  (依赖端口接口，不依赖实现)                        │
└─────────────────────────────────────────────────────────────────┘
                               │
              ┌────────────────┴────────────────┐
              ▼                                 ▼
┌──────────────────────────┐    ┌──────────────────────────────────┐
│     领域层 (domains/)     │    │        端口层 (ports/)            │
│      领域模型/实体         │    │         抽象接口定义              │
│        业务逻辑           │    │    (仓库接口、服务接口等)          │
└──────────────────────────┘    └──────────────────────────────────┘
                                                │
                                                ▼
                              ┌──────────────────────────────────────┐
                              │       适配器层 (adapters/)            │
                              │   (实现端口接口 - Driven Adapter)     │
                              │   数据库、消息队列、外部API等         │
                              └──────────────────────────────────────┘
```

**依赖方向**: 外层依赖内层，内层不依赖外层。领域层位于核心，完全独立。

---

## 快速开始

### 安装依赖

```bash
make install
```

### 运行应用

```bash
make run
```

### 开发模式（自动重载）

```bash
make run-dev
```

### 运行测试

```bash
make test
```

### 配置环境变量

创建 `.env` 文件：

```bash
DIP_HUB_PORT=8000
DIP_HUB_DEBUG=true
DIP_HUB_LOG_LEVEL=DEBUG
```

---

## 扩展指南

### 添加新的领域模型

1. 在 `src/domains/` 创建新的领域模型文件
2. 定义数据类和业务逻辑

### 添加新的端口

1. 在 `src/ports/` 创建新的端口接口文件
2. 定义抽象基类和方法签名

### 添加新的适配器

1. 在 `src/adapters/` 创建新的适配器
2. 实现对应的端口接口
3. 在 `src/infrastructure/container.py` 中注册适配器

### 添加新的API端点

1. 在 `src/routers/schemas/` 创建请求/响应模型
2. 在 `src/routers/` 创建新的路由文件
3. 在 `main.py` 中注册路由

---

## 参考资料

- [六边形架构（端口-适配器架构）](https://alistair.cockburn.us/hexagonal-architecture/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

