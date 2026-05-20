# NetManager - 网络设备管理系统

一个功能完整的网络设备管理系统，包含设备管理、配置备份、监控告警等功能。

## 技术栈

### 后端
- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite（开发环境）
- Uvicorn

### 前端
- Vue 3 (Composition API)
- Vue Router
- Pinia
- Element Plus
- ECharts
- Vite

## 功能特性

1. **用户认证与权限**
   - 登录/登出
   - 管理员与只读用户权限

2. **设备管理**
   - 设备CRUD操作
   - 设备搜索与筛选
   - 设备状态展示

3. **设备详情**
   - 基本信息展示
   - 端口列表
   - 配置备份与查看
   - 监控指标图表

4. **配置管理**
   - 配置备份
   - 配置历史查看

5. **监控与告警**
   - 仪表板统计
   - 告警中心
   - 操作日志

## 快速开始

### 使用 Docker（推荐）

1. 克隆项目
```bash
git clone <repo-url>
cd netmanager
```

2. 启动服务
```bash
docker-compose up -d
```

3. 访问应用
- 前端: http://localhost:5173
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

### 手动启动

#### 后端

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端

```bash
cd frontend
npm install
npm run dev
```

## 默认账号

- **管理员**: `admin` / `admin123`
- **观察者**: `viewer` / `viewer123`

## 项目结构

```
netmanager/
├── backend/
│   ├── app/
│   │   ├── api/           # API 路由
│   │   ├── core/          # 核心配置
│   │   ├── models/        # 数据模型
│   │   └── schemas/       # Pydantic 模式
│   ├── main.py            # 应用入口
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/           # API 调用
│   │   ├── components/    # 组件
│   │   ├── layouts/       # 布局
│   │   ├── router/        # 路由
│   │   ├── stores/        # 状态管理
│   │   └── views/         # 页面
│   └── package.json
└── docker-compose.yml
```

## 开发说明

### API 端点

- `POST /api/login` - 用户登录
- `GET /api/devices` - 获取设备列表
- `POST /api/devices` - 创建设备
- `PUT /api/devices/{id}` - 更新设备
- `DELETE /api/devices/{id}` - 删除设备
- `GET /api/devices/{id}/configs` - 获取设备配置
- `POST /api/devices/{id}/backup_config` - 备份设备配置
- `GET /api/devices/{id}/ports` - 获取设备端口
- `GET /api/devices/{id}/metrics` - 获取监控指标
- `GET /api/dashboard/stats` - 获取仪表板统计
- `GET /api/alerts` - 获取告警
- `PUT /api/alerts/{id}/resolve` - 解决告警
- `GET /api/logs` - 获取操作日志

## 许可证

MIT
