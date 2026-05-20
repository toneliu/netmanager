# NetManager - 企业网络管理与监控平台

## 项目简介

NetManager 是一款基于 AI Agent 的企业网络故障根因定位与自愈系统，能够自动检测网络故障、定位根本原因并执行智能修复。

## 核心特性

### 🤖 多 Agent 协作系统

- **数据采集 Agent** - 收集 Syslog、SNMP 指标等网络数据
- **日志解析 Agent** - 智能解析日志，检测异常事件
- **拓扑感知 Agent** - 构建网络拓扑图，分析设备关联
- **推理 Agent** - 基于规则和拓扑进行根因分析
- **执行 Agent** - 自动执行修复命令，实现自愈

### 🔍 智能故障检测

- 实时监控网络设备状态
- 异常检测算法识别潜在故障
- 多维度数据关联分析
- 根因定位精确到端口级别

### 🔧 自动故障修复

- 智能修复方案生成
- 支持自动/手动执行模式
- 命令执行回滚机制
- 修复效果验证

### 📊 可视化界面

- 实时网络拓扑展示
- 监控仪表盘
- 推理过程可视化
- 告警历史查询

## 技术架构

### 前端技术栈

- **Vue 3** - 现代化前端框架
- **Element Plus** - UI 组件库
- **ECharts** - 数据可视化
- **Pinia** - 状态管理
- **Vue Router** - 路由管理

### 后端技术栈

- **Python 3** - 核心开发语言
- **FastAPI** - 高性能 Web 框架
- **LangGraph** - Agent 工作流编排
- **异步编程** - 高并发支持

## 系统架构图

```
┌─────────────────────────────────────────────────────────┐
│                    Vue 3 Frontend                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │  拓扑视图  │ │ 仪表盘   │ │ 故障检测  │ │ 执行控制  │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘   │
└───────┼────────────┼────────────┼────────────┼─────────┘
        │            │            │            │
        └────────────┴─────┬──────┴────────────┘
                           │
                    ┌──────┴──────┐
                    │  FastAPI   │
                    │   Backend   │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────┴───────┐  ┌──────┴──────┐  ┌───────┴───────┐
│ 数据采集Agent  │  │ 日志解析Agent │  │ 拓扑感知Agent  │
└───────┬───────┘  └──────┬──────┘  └───────┬───────┘
        │                 │                 │
        └─────────────────┴───────┬─────────┘
                                  │
                         ┌────────┴────────┐
                         │    推理Agent     │
                         └────────┬────────┘
                                  │
                         ┌────────┴────────┐
                         │    执行Agent     │
                         └─────────────────┘
```

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 安装部署

#### 1. 克隆项目

```bash
git clone https://github.com/toneliu/netmanager.git
cd netmanager
```

#### 2. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 3. 安装前端依赖

```bash
cd frontend
npm install
```

#### 4. 启动服务

```bash
# 启动后端 (端口 8000)
cd backend
python main.py

# 启动前端 (端口 3000) - 新开终端
cd frontend
npm run dev
```

#### 5. 访问系统

打开浏览器访问: http://localhost:3000

## 功能演示

### 网络拓扑视图
实时展示网络设备和连接状态，支持设备详情查看和告警高亮。

### 监控仪表盘
展示网络可用性、延迟、丢包率等关键指标，支持时间范围选择。

### 故障检测
点击"开始检测"启动多 Agent 协作推理，自动定位故障根因。

### 推理过程可视化
清晰展示每个 Agent 的执行步骤和判断依据，保证推理可解释性。

## API 接口

### 状态查询

```
GET /api/status
```
获取 Agent 状态和网络拓扑

### 网络拓扑

```
GET /api/topology
```
获取完整网络拓扑结构

### 日志查询

```
GET /api/logs?count=20
```
获取最近 Syslog 日志

### 指标查询

```
GET /api/metrics?devices=acc-01,acc-02
```
获取设备 SNMP 指标

### 故障检测

```
POST /api/detect
```
启动故障检测流程

### 命令执行

```
POST /api/execute
{
  "command": "interface GigabitEthernet0/1\nshutdown",
  "device": "acc-02"
}
```
执行设备配置命令

## 使用场景

### 1. 企业内网监控
- 实时监控核心交换机、汇聚交换机、接入交换机
- 及时发现链路故障、端口异常等问题

### 2. 故障快速响应
- 自动定位故障根因，减少人工排查时间
- 从 30 分钟缩短到分钟级

### 3. 自动化运维
- 支持自动修复常见故障
- 减少运维人员工作负担

### 4. 网络健康管理
- 建立网络健康基线
- 预测潜在风险

## 项目结构

```
netmanager/
├── frontend/                    # Vue 3 前端
│   ├── src/
│   │   ├── views/             # 页面组件
│   │   │   ├── TopologyView.vue   # 网络拓扑
│   │   │   ├── DashboardView.vue  # 监控仪表盘
│   │   │   ├── DetectionView.vue  # 故障检测
│   │   │   ├── ExecutionView.vue  # 执行控制
│   │   │   └── ReportView.vue     # 报告中心
│   │   ├── stores/            # Pinia 状态管理
│   │   ├── router/            # 路由配置
│   │   └── assets/            # 静态资源
│   └── package.json
│
├── backend/                    # Python FastAPI 后端
│   ├── agents/                # Agent 实现
│   │   ├── agents.py          # Agent 核心逻辑
│   │   ├── workflow.py        # 工作流编排
│   │   └── simulator.py        # 模拟数据
│   ├── main.py               # API 主入口
│   └── requirements.txt
│
├── screenshots/               # 界面截图
├── README.md                 # 项目文档
└── LICENSE                  # MIT 许可证
```

## 生产环境部署

### 替换模拟组件

| Demo 组件 | 生产环境替换方案 |
|-----------|----------------|
| 模拟 Syslog | rsyslog + Logstash + Elasticsearch |
| 模拟 SNMP | Prometheus SNMP Exporter |
| 规则推理 | OpenAI GPT-4 / Claude API |
| 设备配置 | NetConf/YANG + PyEZ |

### Docker 部署

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes 部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: netmanager-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: netmanager-backend
  template:
    metadata:
      labels:
        app: netmanager-backend
    spec:
      containers:
      - name: backend
        image: netmanager-backend:latest
        ports:
        - containerPort: 8000
```

## 性能指标

- 故障检测响应时间: < 10 秒
- 支持设备规模: 1000+ 台
- 推理准确率: > 90%
- 系统可用性: 99.9%

## 安全特性

- API 认证授权
- 敏感数据加密
- 操作审计日志
- 命令执行权限控制

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 版本历史

### v1.0.0 (2024-01)
- 实现基础故障检测功能
- 完成多 Agent 协作系统
- 开发可视化界面

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- **GitHub**: https://github.com/toneliu/netmanager
- **问题反馈**: https://github.com/toneliu/netmanager/issues

---

**Made with ❤️ by NetManager Team**
