# 基于现有环境的Docker部署指南

本文档介绍如何在已有MySQL8、we-mp-rss服务和werss-net网络的环境中部署微信公众号RSS合并服务。

## 📋 环境要求

- 已安装Docker和Docker Compose
- 已存在werss-net网络
- 已部署MySQL8服务（可选）
- 已部署we-mp-rss服务（可选）

## 🚀 快速部署

### 1. 检查现有环境

```bash
# 检查网络
docker network ls | grep werss-net

# 检查现有服务
docker ps | grep -E "(mysql8|we-mp-rss)"

# 如果没有werss-net网络，创建它
docker network create werss-net
```

### 2. 部署服务

```bash
# 给脚本执行权限
chmod +x scripts/deploy-with-existing.sh

# 启动服务
./scripts/deploy-with-existing.sh start

# 检查状态
./scripts/deploy-with-existing.sh status

# 查看日志
./scripts/deploy-with-existing.sh logs
```

### 3. 验证部署

```bash
# 测试健康检查
curl http://localhost:8002/health

# 测试API接口
curl http://localhost:8002/generate

# 查看网络信息
./scripts/deploy-with-existing.sh network
```

## 📁 服务配置

### 服务架构

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Nginx     │    │  Flask App  │    │   MySQL8    │
│   (80/443)  │◄──►│   (8002)    │◄──►│   (3306)    │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 端口映射

| 服务 | 容器端口 | 主机端口 | 说明 |
|------|----------|----------|------|
| Nginx | 80, 443 | 80, 443 | HTTP/HTTPS访问 |
| Flask App | 8002 | 8002 | 直接API访问 |
| MySQL8 | 3306 | 3306 | 数据库访问 |

### 网络配置

- **网络名称**: werss-net (外部网络)
- **网络类型**: bridge
- **容器连接**: 所有服务都连接到werss-net网络

## 🔧 数据库配置

### 默认数据库信息

- **主机**: mysql8 (容器内)
- **端口**: 3306
- **数据库**: wewe-rss
- **用户名**: wxmp
- **密码**: wxmp123
- **Root密码**: StrongPass123!

### 数据库连接

```bash
# 连接到MySQL8容器
docker exec -it mysql8 mysql -u root -p

# 查看数据库
SHOW DATABASES;
USE wewe-rss;
SHOW TABLES;
```

## 📝 管理命令

### 服务管理

```bash
# 启动服务
./scripts/deploy-with-existing.sh start

# 停止服务
./scripts/deploy-with-existing.sh stop

# 重启服务
./scripts/deploy-with-existing.sh restart

# 查看状态
./scripts/deploy-with-existing.sh status

# 查看日志
./scripts/deploy-with-existing.sh logs

# 查看网络信息
./scripts/deploy-with-existing.sh network

# 备份数据
./scripts/deploy-with-existing.sh backup

# 清理资源
./scripts/deploy-with-existing.sh cleanup
```

### Docker命令

```bash
# 查看容器状态
docker-compose ps

# 查看服务日志
docker-compose logs -f wx-mp-rss

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

#### 1. 网络连接问题
```bash
# 检查网络是否存在
docker network ls | grep werss-net

# 创建网络（如果不存在）
docker network create werss-net

# 检查容器网络连接
docker inspect wx-mp-rss-service | grep -A 10 "Networks"
```

#### 2. 数据库连接失败
```bash
# 检查MySQL8容器状态
docker ps | grep mysql8

# 检查数据库连接
docker exec mysql8 mysql -u wxmp -p -e "SELECT 1"

# 查看MySQL日志
docker logs mysql8
```

#### 3. 服务启动失败
```bash
# 检查容器状态
docker-compose ps

# 查看详细日志
docker-compose logs wx-mp-rss

# 检查端口占用
netstat -tlnp | grep :8002
```

#### 4. 现有服务冲突
```bash
# 检查现有服务
docker ps | grep -E "(we-mp-rss|mysql8)"

# 停止冲突的服务
docker stop we-mp-rss mysql8

# 或者使用不同的容器名称
# 修改docker-compose.yml中的container_name
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
./scripts/deploy-with-existing.sh restart
```

### 更新配置

```bash
# 修改配置文件
vim config/config.docker.yaml

# 重启服务
./scripts/deploy-with-existing.sh restart
```

### 数据库迁移

```bash
# 备份当前数据
./scripts/deploy-with-existing.sh backup

# 执行迁移脚本
docker-compose exec mysql8 mysql -u root -p wewe-rss < migration.sql
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
./scripts/deploy-with-existing.sh backup
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
3. 运行 `./scripts/deploy-with-existing.sh status` 检查状态
4. 运行 `./scripts/deploy-with-existing.sh network` 检查网络

---

**注意**: 此配置使用现有的werss-net网络和MySQL8服务，确保它们已正确配置！ 