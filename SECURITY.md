# 安全配置说明

## 概述

本服务实现了多层安全保护机制，确保API接口的安全性和稳定性。

## 安全功能

### 1. API密钥认证

**功能说明：**
- 所有敏感接口都需要API密钥认证
- 支持请求头方式和URL参数方式传递密钥
- 密钥验证失败会记录安全事件日志

**配置项：**
```yaml
security:
  api_key_required: true
  api_key: "your-secret-api-key-2024"
```

**使用方法：**
```bash
# 请求头方式
curl -H "X-API-Key: your-secret-api-key-2024" http://localhost:8080/generate

# URL参数方式
curl "http://localhost:8080/generate?api_key=your-secret-api-key-2024"
```

### 2. 请求频率限制

**功能说明：**
- 防止API被恶意滥用
- 基于IP地址进行限制
- 支持配置时间窗口和请求次数

**配置项：**
```yaml
security:
  rate_limit_enabled: true
  rate_limit_requests: 10  # 每分钟请求次数
  rate_limit_window: 60    # 时间窗口（秒）
```

**限制规则：**
- 生成接口：每分钟最多10次请求
- 下载接口：每分钟最多10次请求
- 健康检查：无限制

### 3. IP白名单（可选）

**功能说明：**
- 可选择性启用IP白名单功能
- 只允许指定IP地址访问
- 支持本地地址和服务器地址

**配置项：**
```yaml
security:
  ip_whitelist_enabled: false
  ip_whitelist: ["127.0.0.1", "localhost"]
```

### 4. 请求验证

**功能说明：**
- 验证请求方法（只允许GET/POST）
- 限制请求体大小（最大16MB）
- 防止恶意请求

### 5. 错误处理

**功能说明：**
- 统一的错误响应格式
- 详细的错误信息记录
- 防止敏感信息泄露

## 安全最佳实践

### 1. 密钥管理

- **定期更换密钥**：建议每月更换一次API密钥
- **密钥复杂度**：使用足够复杂的密钥（至少32位）
- **密钥存储**：不要在代码中硬编码密钥，使用环境变量

```bash
# 设置环境变量
export API_KEY="your-new-secret-key-2024"
```

### 2. 网络安全

- **HTTPS**：生产环境必须使用HTTPS
- **防火墙**：配置防火墙只允许必要端口
- **代理**：使用反向代理（如Nginx）增加安全层

### 3. 监控和日志

- **安全事件监控**：监控API密钥验证失败、频率限制触发等事件
- **访问日志**：记录所有API访问日志
- **异常告警**：设置异常访问告警机制

### 4. 配置建议

**开发环境：**
```yaml
security:
  api_key_required: true
  api_key: "dev-secret-key-2024"
  rate_limit_enabled: true
  rate_limit_requests: 100
  ip_whitelist_enabled: false
```

**生产环境：**
```yaml
security:
  api_key_required: true
  api_key: "${API_KEY}"  # 使用环境变量
  rate_limit_enabled: true
  rate_limit_requests: 10
  ip_whitelist_enabled: true
  ip_whitelist: ["your-allowed-ips"]
```

## 安全测试

运行安全测试脚本验证安全功能：

```bash
python test_security.py
```

测试内容包括：
- API密钥认证测试
- 请求频率限制测试
- 请求验证测试
- 文件下载安全测试
- 错误处理测试

## 故障排除

### 常见问题

1. **401 Unauthorized**
   - 检查API密钥是否正确
   - 确认密钥传递方式（请求头或URL参数）

2. **429 Too Many Requests**
   - 请求频率超限，等待一段时间后重试
   - 检查是否被恶意攻击

3. **403 Forbidden**
   - IP地址不在白名单中
   - 检查IP白名单配置

### 日志分析

查看安全事件日志：
```bash
# 查看包含安全事件的日志
grep "安全事件" logs/app.log
```

## 更新日志

- **v1.0.0**：初始安全功能实现
  - API密钥认证
  - 请求频率限制
  - IP白名单支持
  - 请求验证
  - 错误处理 