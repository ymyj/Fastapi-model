# FastAPI Best Architecture 项目文档

## 项目简介

基于 **FastAPI + Vue3 + MySQL + Redis** 构建的企业级全栈管理系统。采用前后端分离架构，融合 Python 后端框架 FastAPI 和前端主流框架 Vue3 实现多端统一开发，提供了一站式开箱即用的开发体验。

---

## 技术栈

### 后端

| 技术 | 版本 | 说明 |
|------|------|------|
| **Python** | 3.11+ | 运行环境 |
| **FastAPI** | >= 0.136.1 | 高性能异步 Web 框架 |
| **Pydantic** | >= 2.13.3 | 数据验证与配置管理 |
| **SQLAlchemy** | >= 2.0.49 | 异步 ORM |
| **Celery** | >= 5.6.3 | 异步任务调度 |
| **Redis** | >= 7.4.0 | 缓存、会话存储、消息队列 |
| **python-jose** | >= 3.5.0 | JWT 认证 |
| **bcrypt** | >= 5.0.0 | 密码加密 |
| **Loguru** | >= 0.7.3 | 结构化日志 |
| **OpenTelemetry** | >= 1.41.1 | 分布式追踪 |
| **Prometheus** | >= 0.25.0 | 指标采集 |
| **python-socketio** | >= 5.16.1 | WebSocket 实时通信 |
| **uvicorn** | >= 0.12.0 | ASGI 服务器 |
| **Alembic** | >= 1.18.4 | 数据库迁移 |
| **Jinja2** | >= 3.1.6 | 模板引擎（代码生成器） |

### 前端

| 技术 | 说明 |
|------|------|
| **Vue 3** | 渐进式 JavaScript 框架 |
| **TypeScript** | 类型安全的 JavaScript 超集 |
| **Vben Admin** | 基于 Ant Design Vue 的企业级后台模板 |
| **Vite** | 下一代前端构建工具 |
| **pnpm** | 高效的 npm 包管理工具 |
| **Socket.IO** | 实时双向通信 |

### 数据库

| 技术 | 版本 | 说明 |
|------|------|------|
| **MySQL** | 8.0+ | 关系型数据库（默认） |
| **PostgreSQL** | 14+ | 关系型数据库（可选） |
| **Redis** | 7.0+ | 缓存与消息中间件 |

---

## 项目结构

```
fastapi-best-architecture/
├── backend/                    # FastAPI 后端项目
│   ├── main.py                 # 应用入口
│   ├── cli.py                  # 命令行工具
│   ├── core/                   # 核心配置层
│   │   ├── conf.py             # 全局配置（pydantic-settings）
│   │   └── registrar.py        # 路由注册
│   ├── database/               # 数据库连接层
│   │   ├── db.py               # SQLAlchemy 异步引擎
│   │   └── redis.py            # Redis 客户端
│   ├── common/                 # 公共基础设施层
│   │   ├── cache/              # 缓存（L1本地 + L2 Redis）
│   │   ├── exception/          # 异常定义与处理器
│   │   ├── observability/      # 可观测性（Prometheus + OpenTelemetry）
│   │   ├── security/           # 安全层（JWT, RBAC, 权限）
│   │   └── ...                 # 其他公共模块
│   ├── middleware/             # 中间件链
│   ├── plugin/                 # 插件系统
│   │   ├── core.py             # 插件核心
│   │   ├── code_generator/     # 代码生成器
│   │   ├── config/             # 系统参数配置
│   │   ├── dict/               # 数据字典
│   │   ├── email/              # 邮件发送
│   │   ├── notice/             # 通知公告
│   │   └── oauth2/             # OAuth2 登录
│   ├── app/                    # 业务应用层
│   │   ├── admin/              # 后台管理模块
│   │   │   ├── api/v1/         # 路由层
│   │   │   ├── crud/           # 数据访问层（DAO）
│   │   │   ├── model/          # ORM 模型层
│   │   │   ├── schema/         # 数据验证层（DTO）
│   │   │   └── service/        # 业务逻辑层
│   │   └── task/               # 异步任务模块（Celery）
│   ├── utils/                  # 通用工具函数
│   ├── alembic/                # 数据库迁移
│   └── .env                    # 环境变量配置
├── frontend/                   # Vue3 前端项目（fastapi-best-architecture-ui）
│   ├── apps/web-antdv-next/    # 主应用
│   ├── internal/               # 内部构建配置
│   ├── packages/               # 公共组件包
│   ├── pnpm-workspace.yaml     # pnpm 工作区配置
│   └── turbo.json              # Turborepo 配置
└── pyproject.toml              # Python 项目配置
```

---

## 环境配置

### 后端配置（`.env`）

```ini
# 环境
ENVIRONMENT='dev'

# MySQL 数据库
DATABASE_TYPE='mysql'
DATABASE_HOST='127.0.0.1'
DATABASE_PORT=3306
DATABASE_USER='root'
DATABASE_PASSWORD='your_password'

# Redis
REDIS_HOST='127.0.0.1'
REDIS_PORT=6379
REDIS_PASSWORD=''
REDIS_DATABASE=0

# Token 密钥（自动生成）
TOKEN_SECRET_KEY='your_secret_key'

# Celery 任务队列
CELERY_BROKER_REDIS_DATABASE=1
```

### 前端配置

- **开发环境**：`frontend/apps/web-antdv-next/.env.development`
- **生产环境**：`frontend/apps/web-antdv-next/.env.production`

---

## 快速启动

### 前置条件

| 环境 | 版本要求 |
|------|----------|
| **Python** | >= 3.10（推荐 3.11+） |
| **Node.js** | >= 18（LTS） |
| **MySQL** | >= 8.0 |
| **Redis** | >= 7.0 |
| **pnpm** | >= 9.0 |

### 第一步：初始化后端数据库

```bash
# 1. 创建 MySQL 数据库
mysql -u root -p -e "CREATE DATABASE fba CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. 安装 Python 依赖（推荐 conda 环境）
conda create -n FastAPI python=3.11 -y
conda activate FastAPI

# 3. 安装项目依赖
cd fastapi-best-architecture
pip install -e .

# 4. 初始化数据库
python -m backend.cli init
# 按提示输入 y 确认初始化
```

### 第二步：启动后端服务

```bash
# 使用 uvicorn 启动
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 或使用 fba CLI
python -m backend.cli run
```

启动成功后访问：
- **API 文档**：http://localhost:8000/docs
- **备用文档**：http://localhost:8000/redoc

### 第三步：启动前端服务

```bash
# 1. 安装 pnpm（如未安装）
npm install -g pnpm

# 2. 进入前端目录
cd frontend

# 3. 安装依赖
pnpm install

# 4. 启动开发服务器
pnpm dev
```

启动成功后访问：http://localhost:5173

### 第四步：登录系统

使用默认管理员账号登录：

| 字段 | 值 |
|------|------|
| 用户名 | `admin` |
| 密码 | `123456` |

---

## 架构设计

### 分层架构

```
┌─────────────────────────────────────────────────────┐
│                   API Layer (路由)                    │
│  - 接收请求，参数校验，调用 Service，返回统一响应       │
│  - 使用 Depends() 进行 JWT/RBAC 鉴权                   │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                  Service Layer (业务逻辑)              │
│  - 核心业务逻辑、事务控制、缓存处理                      │
│  - 调用 CRUD 进行数据库操作                            │
──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                   CRUD Layer (数据访问)                │
│  - 继承 CRUDPlus，封装 SQLAlchemy 操作                 │
│  - 提供 select/insert/update/delete 方法              │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                   Model Layer (ORM模型)               │
│  - 继承 Base（含 DateTimeMixin + UserMixin）          │
│  - 定义表结构和关系                                    │
└─────────────────────────────────────────────────────┘
```

### 插件化架构

项目设计了**两级插件系统**：
- **扩展级插件 (extend)**：注入到现有应用模块中（如 `config`、`dict`）
- **应用级插件 (app)**：作为独立模块注册到主路由（如 `code_generator`、`oauth2`）

### RBAC 权限模型

```
用户 (User) ↔ 角色 (Role) ↔ 菜单 (Menu) / 权限标识 (perms)
角色 (Role) ↔ 数据范围 (DataScope) ↔ 数据规则 (DataRule)
```

支持基于数据范围的精细数据过滤：
- 全部数据、本部门数据、本部门及以下、仅本人数据、自定义规则

---

## 路由结构

```
/api/v1
├── /auth                        # 认证模块
│   ├── POST /login              # 用户登录
│   ├── POST /refresh            # 刷新 Token
│   ├── POST /logout             # 登出
│   └── GET  /captcha            # 验证码
├── /sys                         # 系统管理
│   ├── /users                   # 用户 CRUD
│   ├── /roles                   # 角色 CRUD
│   ├── /menus                   # 菜单 CRUD
│   ├── /depts                   # 部门 CRUD
│   ── /files                   # 文件管理
├── /logs                        # 日志模块
│   ├── /login-logs              # 登录日志
│   └── /opera-logs              # 操作日志
├── /monitor                     # 监控模块
│   ├── /online                  # 在线用户
│   ├── /redis                   # Redis 监控
│   └── /server                  # 服务器监控
── [插件路由]                    # 动态注入
    ├── /configs                 # 参数配置
    ├── /dict-types + /dict-data # 数据字典
    ├── /code-gen                # 代码生成
    ├── /notices                 # 通知公告
    ├── /emails                  # 邮件
    └── /oauth2                  # OAuth2
```

---

## 开发工具

| 工具 | 用途 |
|------|------|
| **Navicat** | MySQL 数据库可视化管理 |
| **Another Redis Desktop Manager** | Redis 可视化管理 |
| **VS Code / PyCharm** | 代码编辑器 |
| **Trae AI** | AI 辅助开发 |

---

## 常见问题

### 1. 数据库初始化失败

```bash
# 手动执行初始化
python -m backend.cli init
# 按提示选择 mysql，输入数据库密码，输入 y 确认
```

### 2. Redis 连接失败

```bash
# 检查 Redis 是否运行
redis-cli ping
# 应返回 PONG
```

### 3. 前端登录失败

检查后端服务是否正常运行，以及前端配置的 API 地址是否正确。

---

## 许可证

MIT License

---

## 致谢

- [FastAPI Best Architecture](https://github.com/fastapi-practices/fastapi-best-architecture)
- [Vben Admin](https://github.com/vbenjs/vue-vben-admin)
- [Vue.js](https://vuejs.org/)
