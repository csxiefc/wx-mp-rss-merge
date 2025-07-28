# 微信公众号RSS合并服务 - Docker部署指南

本文档介绍如何在CentOS 8上使用Docker Compose部署微信公众号RSS合并服务。

## 📋 系统要求

- CentOS 8 或更高版本
- 至少 2GB RAM
- 至少 10GB 可用磁盘空间
- 网络连接（用于下载Docker镜像）

## 🚀 快速开始

### 1. 安装Docker环境

```bash
# 下载项目
git clone <your-repo-url>
cd wx-mp-rss-merge

# 安装Docker（需要root权限）
sudo chmod +x scripts/install_docker_centos8.sh
sudo ./scripts/install_docker_centos8.sh

# 重新登录以应用docker组权限
newgrp docker
```

### 2. 启动服务

```bash
# 启动所有服务
chmod +x scripts/deploy.sh
./scripts/deploy.sh start
```

### 3. 验证部署

```bash
# 检查服务状态
./scripts/deploy.sh status

# 查看日志
./scripts/deploy.sh logs

# 测试API
curl http://localhost:8002/health
```

## 📁 项目结构

```
wx-mp-rss-merge/
├── Dockerfile                    # Docker镜像构建文件
├── docker-compose.yml           # Docker Compose配置
├── .dockerignore                # Docker忽略文件
├── config/
│   ├── config.yaml             # 开发环境配置
│   └── config.docker.yaml      # Docker环境配置
├── nginx/
│   └── nginx.conf              # Nginx反向代理配置
├── mysql/
│   └── init/
│       └── 01-init.sql         # MySQL初始化脚本
├── scripts/
│   ├── deploy.sh               # 部署脚本
│   └── install_docker_centos8.sh # Docker安装脚本
└── storage/                    # 文件存储目录
```

## 🔧 服务配置

### 服务架构

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Nginx     │    │  Flask App  │    │   MySQL     │
│   (80/443)  │◄──►│   (8080)    │◄──►│   (3306)    │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 端口映射

| 服务 | 容器端口 | 主机端口 | 说明 |
|------|----------|----------|------|
| Nginx | 80, 443 | 80, 443 | HTTP/HTTPS访问 |
| Flask App | 8002 | 8002 | 直接API访问 |
| MySQL | 3306 | 3306 | 数据库访问 |

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| ENVIRONMENT | production | 运行环境 |
| PYTHONPATH | /app | Python路径 |
| PYTHONUNBUFFERED | 1 | Python输出缓冲 |

## 📊 数据库配置

### 默认数据库信息

- **主机**: mysql (容器内)
- **端口**: 3306
- **数据库**: wewe-rss
- **用户名**: wxmp
- **密码**: wxmp123
- **Root密码**: StrongPass123!

### 数据库表结构

#### feeds表（微信公众号信息）
```sql
CREATE TABLE feeds (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mp_id VARCHAR(100) UNIQUE NOT NULL,
    mp_name VARCHAR(200) NOT NULL,
    mp_intro TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### articles表（文章信息）
```sql
CREATE TABLE articles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mp_id VARCHAR(100) NOT NULL,
    title VARCHAR(500) NOT NULL,
    url VARCHAR(1000) NOT NULL,
    content LONGTEXT,
    description TEXT,
    publish_time INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 🔐 安全配置

### API密钥认证
- **API密钥认证**: 已禁用
- **说明**: 服务已配置为无需API密钥认证

### 请求频率限制
- **限制**: 每分钟10次请求
- **时间窗口**: 60秒

### 防火墙配置
- 开放端口: 80, 443, 8002, 3306
- 使用firewalld管理

## 📝 管理命令

### 服务管理

```bash
# 启动服务
./scripts/deploy.sh start

# 停止服务
./scripts/deploy.sh stop

# 重启服务
./scripts/deploy.sh restart

# 查看状态
./scripts/deploy.sh status

# 查看日志
./scripts/deploy.sh logs

# 清理资源
./scripts/deploy.sh cleanup

# 备份数据
./scripts/deploy.sh backup
```

### Docker命令

```bash
# 查看容器状态
docker-compose ps

# 查看服务日志
docker-compose logs -f

# 进入容器
docker-compose exec wx-mp-rss bash

# 重启特定服务
docker-compose restart wx-mp-rss

# 更新镜像
docker-compose pull
docker-compose up -d
```

## 🔍 故障排除

### 常见问题

#### 1. 服务启动失败
```bash
# 检查容器状态
docker-compose ps

# 查看详细日志
docker-compose logs wx-mp-rss

# 检查端口占用
netstat -tlnp | grep :8002
```

#### 2. 数据库连接失败
```bash
# 检查MySQL容器
docker-compose logs mysql

# 进入MySQL容器测试
docker-compose exec mysql mysql -u root -p

# 检查网络连接
docker-compose exec wx-mp-rss ping mysql
```

#### 3. 文件权限问题
```bash
# 修复存储目录权限
sudo chown -R 1000:1000 storage/
sudo chmod -R 755 storage/
```

#### 4. 内存不足
```bash
# 检查系统资源
free -h
df -h

# 清理Docker资源
docker system prune -a
```

### 日志位置

- **应用日志**: `logs/app.log`
- **Nginx日志**: 容器内 `/var/log/nginx/`
- **MySQL日志**: 容器内 `/var/log/mysql/`

## 🔄 更新部署

### 更新应用

```bash
# 拉取最新代码
git pull

# 重新构建并启动
./scripts/deploy.sh restart
```

### 更新配置

```bash
# 修改配置文件
vim config/config.docker.yaml

# 重启服务
./scripts/deploy.sh restart
```

### 数据库迁移

```bash
# 备份当前数据
./scripts/deploy.sh backup

# 执行迁移脚本
docker-compose exec mysql mysql -u root -p wewe-rss < migration.sql
```

## 📈 监控和维护

### 健康检查

```bash
# 检查服务健康状态
curl http://localhost:8002/health

# 检查容器健康状态
docker-compose ps
```

### 性能监控

```bash
# 查看容器资源使用
docker stats

# 查看系统资源
htop
```

### 定期维护

```bash
# 清理日志文件
find logs/ -name "*.log" -mtime +7 -delete

# 清理Docker资源
docker system prune -f

# 备份数据
./scripts/deploy.sh backup
```

## 🛡️ 安全建议

1. **修改默认密码**: 更改MySQL和API密钥的默认密码
2. **配置SSL**: 在生产环境中启用HTTPS
3. **限制访问**: 配置防火墙规则限制访问来源
4. **定期更新**: 定期更新Docker镜像和系统包
5. **监控日志**: 定期检查日志文件发现异常

## 📞 技术支持

如果遇到问题，请：

1. 检查日志文件
2. 查看本文档的故障排除部分
3. 提交Issue到项目仓库

---

**注意**: 生产环境部署前请务必修改默认密码和配置！ 