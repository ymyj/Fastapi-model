# FastAPI 全栈管理系统

基于 **FastAPI + Vue3 + MySQL + Redis** 构建的企业级全栈管理系统，采用前后端分离架构，提供完整的管理功能与实时数据模拟能力。

---

## 📁 项目结构

```
├── fastapi-best-architecture/        # FastAPI 后端项目
│   ├── backend/                      # 后端核心代码
│   │   ├── api/                      # API 路由层
│   │   ├── core/                     # 核心配置与公共组件
│   │   ├── database/                 # 数据库连接（MySQL + Redis）
│   │   ├── middleware/               # 中间件（鉴权、日志、CORS 等）
│   │   ├── plugin/                   # 插件系统
│   │   ├── app/                      # 业务模块（用户、角色、权限、任务等）
│   │   ├── cli.py                    # 命令行工具
│   │   └── main.py                   # 应用入口
│   └── .env                          # 环境变量配置
├── fastapi-best-architecture-ui/     # Vue3 前端项目（Vben Admin）
│   ├── apps/web-antdv-next/          # 主应用
│   ├── packages/                     # 公共组件包
│   └── pnpm-workspace.yaml           # Monorepo 配置
├── pyproject.toml                    # Python 项目配置
└── README.md                         # 本文档
```

---

## 🛠 技术栈

### 后端

| 技术 | 说明 |
|------|------|
| **FastAPI** | 高性能异步 Web 框架 |
| **SQLAlchemy 2.0** | 异步 ORM |
| **Pydantic 2** | 数据验证与配置管理 |
| **MySQL 8.0** | 关系型数据库 |
| **Redis 7** | 缓存与会话管理 |
| **Celery** | 异步任务调度 |
| **python-jose** | JWT 认证 |
| **Loguru** | 结构化日志 |
| **OpenTelemetry** | 分布式追踪 |
| **Prometheus** | 指标采集 |

### 前端

| 技术 | 说明 |
|------|------|
| **Vue 3** | 渐进式 JavaScript 框架 |
| **TypeScript** | 类型安全 |
| **Vben Admin** | 企业级后台模板 |
| **Ant Design Vue** | UI 组件库 |
| **Vite** | 构建工具 |
| **pnpm** | 包管理工具 |

### 模拟插件

| 技术 | 说明 |
|------|------|
| **NumPy** | 数值计算 |
| **Matplotlib** | 科学可视化 |
| **Socket.IO** | 实时通信 |
| **Vue 3** | 前端交互 |

---

## 🚀 快速开始

### 前置条件

| 环境 | 版本要求 |
|------|----------|
| Python | >= 3.10 |
| Node.js | >= 18 |
| MySQL | >= 8.0 |
| Redis | >= 7.0 |
| pnpm | >= 9.0 |

### 后端启动

```bash
# 1. 创建 Python 环境
conda create -n FastAPI python=3.11 -y
conda activate FastAPI

# 2. 安装依赖
cd fastapi-best-architecture
pip install -e .

# 3. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 .env 文件，填写数据库密码等信息

# 4. 初始化数据库
python -m backend.cli init

# 5. 启动服务
python -m uvicorn backend.main:app --reload --port 8000
```

### 前端启动

```bash
# 1. 安装 pnpm
npm install -g pnpm

# 2. 安装依赖并启动
cd frontend
pnpm install
pnpm dev
```

### 默认账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| `admin` | `123456` | 超级管理员 |

---

## 🏗 架构设计

### 分层架构

```
API 层 (路由) → Service 层 (业务逻辑) → CRUD 层 (数据访问) → Model 层 (ORM)
```

### 权限模型

基于 **RBAC** 的四级权限控制：
- 用户 ↔ 角色 ↔ 菜单/按钮 ↔ 数据范围

### 插件化设计

支持热插拔插件，已内置：
- 代码生成器
- 系统参数配置
- 数据字典
- 邮件通知
- OAuth2 登录
- 地下水污染模拟（可独立运行）

---

## 🌐 路由结构

| 路径 | 说明 |
|------|------|
| `/api/v1/auth/*` | 认证（登录、登出、验证码） |
| `/api/v1/sys/*` | 系统管理（用户、角色、菜单、部门） |
| `/api/v1/logs/*` | 日志（登录日志、操作日志） |
| `/api/v1/monitor/*` | 监控（在线用户、Redis、服务器） |
| `/api/v1/tasks/*` | 任务管理（Celery 调度器） |
| `[插件路由]` | 动态注入的插件接口 |

---

## 📝 许可证

MIT License

---

## 🙏 致谢

- [FastAPI Best Architecture](https://github.com/fastapi-practices/fastapi-best-architecture)
- [Vben Admin](https://github.com/vbenjs/vue-vben-admin)
- [Vue.js](https://vuejs.org/)
