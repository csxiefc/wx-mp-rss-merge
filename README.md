# 微信公众号RSS合并服务

这是一个Python Flask应用，用于从MySQL数据库中读取微信公众号和文章数据，生成合并的JSON文件。

## 功能特性

- 从MySQL数据库读取微信公众号信息（feeds表）
- 根据配置获取最近N天的文章数据（articles表）
- 合并feeds和articles数据生成JSON文件
- 提供RESTful API接口
- 支持文件下载
- 自动清理旧文件

## 项目结构

```
wx-mp-rss-merge/
├── src/                    # 源代码目录
│   ├── __init__.py        # 包初始化文件
│   ├── core/              # 核心业务逻辑
│   │   ├── __init__.py
│   │   ├── database.py    # 数据库操作
│   │   └── data_processor.py  # 数据处理
│   ├── api/               # API接口层
│   │   ├── __init__.py
│   │   └── app.py         # Flask应用
│   └── utils/             # 工具模块
│       ├── __init__.py
│       └── file_manager.py # 文件管理
├── tests/                 # 测试目录
│   ├── __init__.py
│   ├── test_database.py   # 数据库测试
│   ├── test_api.py        # API测试
│   └── test_integration.py # 集成测试
├── config/                # 配置文件目录
│   └── config.yaml
├── scripts/               # 脚本目录
│   ├── start_service.bat  # 启动服务脚本
│   └── run_tests.bat      # 运行测试脚本
├── storage/               # 文件存储目录（自动创建）
├── requirements.txt       # Python依赖
├── setup.py              # 安装脚本
├── run.py                # 启动入口
├── README.md             # 项目说明
├── .gitignore           # Git忽略文件
└── 项目总结.md          # 项目总结文档
```

## 安装和配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

或者使用setup.py安装：

```bash
pip install -e .
```

### 2. 配置数据库

编辑 `config/config.yaml` 文件，配置数据库连接信息：

```yaml
database:
  host: "0.0.0.0"
  port: 3306
  user: "root"
  password: "StrongPass123!"
  database: "wewe-rss"
  charset: "utf8mb4"
```

### 3. 配置应用参数

```yaml
app:
  host: "0.0.0.0"
  port: 8002
  debug: true

data:
  recent_days: 3  # 获取最近3天的文章

file:
  storage_path: "./storage"
  url_prefix_prod: "http://0.0.0.0:8002/files"  # 生产环境URL
  url_prefix_dev: "http://localhost:8002/files"       # 开发环境URL
  url_prefix: "http://localhost:8002/files"           # 当前使用的URL（自动设置）
```

### 4. 环境配置

系统会根据 `ENVIRONMENT` 环境变量自动选择合适的URL前缀：

- **开发环境** (`ENVIRONMENT=development`): 使用 `localhost`
- **生产环境** (`ENVIRONMENT=production`): 使用服务器IP
- **默认环境**: 使用 `localhost`（开发环境）

## 启动服务

### 开发环境（默认使用localhost）

#### 方法1：直接运行
```bash
# 设置环境变量
set ENVIRONMENT=development  # Windows
export ENVIRONMENT=development  # Linux/Mac

python run.py
```

#### 方法2：使用脚本
```bash
# Windows
scripts/start_service.bat

# Linux/Mac
ENVIRONMENT=development python run.py
```

### 生产环境（使用服务器IP）

#### 方法1：直接运行
```bash
# 设置环境变量
set ENVIRONMENT=production  # Windows
export ENVIRONMENT=production  # Linux/Mac

python run.py
```

#### 方法2：使用脚本
```bash
# Windows
scripts/start_production.bat

# Linux/Mac
ENVIRONMENT=production python run.py
```

### 方法3：使用安装的命令
```bash
# 开发环境
ENVIRONMENT=development wx-mp-rss

# 生产环境
ENVIRONMENT=production wx-mp-rss
```

## 运行测试

### 方法1：直接运行测试
```bash
# 数据库测试
python tests/test_database.py

# 集成测试
python tests/test_integration.py

# API测试
python tests/test_api.py
```

### 方法2：使用脚本
```bash
# Windows
scripts/run_tests.bat
```

## API接口

### 1. 生成JSON文件

**接口地址：** `GET /generate`

**功能：** 从数据库读取数据并生成JSON文件

**返回格式：**
```json
{
  "code": 200,
  "msg": "成功",
  "fileUrl": "http://localhost:8002/files/result.json",
  "data": {
    "filename": "result.json",
    "record_count": 150,
    "recent_days": 3
  }
}
```

### 2. 下载文件

**接口地址：** `GET /files/<filename>`

**功能：** 下载生成的JSON文件

### 3. 健康检查

**接口地址：** `GET /health`

**功能：** 检查服务状态

### 4. 首页

**接口地址：** `GET /`

**功能：** 显示服务信息和可用接口

## 数据库表结构

### feeds表（微信公众号信息）
```sql
CREATE TABLE `feeds` (
  `id` varchar(255) NOT NULL,
  `mp_name` varchar(255) DEFAULT NULL,
  `mp_cover` varchar(255) DEFAULT NULL,
  `mp_intro` varchar(255) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `sync_time` int DEFAULT NULL,
  `update_time` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `faker_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### articles表（文章信息）
```sql
CREATE TABLE `articles` (
  `id` varchar(255) NOT NULL,
  `mp_id` varchar(255) DEFAULT NULL,
  `title` varchar(500) DEFAULT NULL,
  `pic_url` varchar(500) DEFAULT NULL,
  `url` varchar(500) DEFAULT NULL,
  `content` text,
  `description` varchar(800) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `publish_time` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_export` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

## JSON文件格式

生成的JSON文件是一个数组，每个对象包含以下字段：

```json
[
  {
    "id": "文章ID",
    "mp_id": "公众号ID",
    "mp_name": "公众号名称",
    "mp_intro": "公众号简介",
    "title": "文章标题",
    "url": "文章链接",
    "content": "文章内容（包含HTML标签）",
    "description": "文章描述",
    "publish_time": 1703123456
  }
]
```

**注意：** 每次调用生成接口都会更新同一个 `result.json` 文件，文件URL保持不变。

## 安全功能

### API访问
服务已配置为无需API密钥认证，可直接访问：

```bash
# 直接访问
curl http://localhost:8002/generate
```

### 请求频率限制
- 生成接口：每分钟最多10次请求
- 下载接口：每分钟最多10次请求
- 健康检查：无限制

### IP白名单（可选）
可以在配置文件中启用IP白名单功能。

## 使用示例

### 生成JSON文件
```bash
curl http://localhost:8002/generate
```

### 下载文件
```bash
curl http://localhost:8002/files/result.json
```

### 健康检查
```bash
curl http://localhost:8002/health
```

## 开发指南

### 项目结构说明

- **src/core/**: 核心业务逻辑，包含数据库操作和数据处理
- **src/api/**: API接口层，包含Flask应用和路由定义
- **src/utils/**: 工具模块，包含文件管理等通用功能
- **tests/**: 测试文件，包含单元测试和集成测试
- **config/**: 配置文件目录
- **scripts/**: 脚本文件目录

### 添加新功能

1. 在相应的模块中添加功能代码
2. 在tests目录中添加对应的测试
3. 更新README文档

### 代码规范

- 使用Python 3.8+
- 遵循PEP 8代码规范
- 添加适当的注释和文档字符串
- 编写单元测试

## 注意事项

1. 确保MySQL数据库连接正常
2. 确保服务器有足够的磁盘空间存储JSON文件
3. 建议定期清理storage目录中的旧文件
4. 生产环境建议使用gunicorn等WSGI服务器

## 故障排除

1. **数据库连接失败：** 检查数据库配置和网络连接
2. **文件生成失败：** 检查storage目录权限
3. **服务启动失败：** 检查端口是否被占用
4. **模块导入失败：** 检查Python路径和依赖安装

## 日志

服务运行日志保存在 `app.log` 文件中，可以通过查看日志来诊断问题。

## 许可证

MIT License 