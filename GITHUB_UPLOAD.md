# GitHub上传功能使用说明

## 功能概述

本功能允许在生成`result.json`文件后，自动将其上传到GitHub仓库。支持文件存在时自动替换更新。

## 配置步骤

### 1. 获取GitHub个人访问令牌

1. 登录GitHub
2. 进入 Settings > Developer settings > Personal access tokens > Tokens (classic)
3. 点击 "Generate new token (classic)"
4. 选择权限：
   - `repo` (完整的仓库访问权限)
   - `workflow` (可选，如果需要GitHub Actions)
5. 生成令牌并复制保存

### 2. 设置环境变量

#### Windows
```cmd
set GITHUB_TOKEN=your_github_token_here
```

#### Linux/Mac
```bash
export GITHUB_TOKEN=your_github_token_here
```

### 3. 配置文件

编辑 `config/config.yaml` 文件，确保GitHub配置正确：

```yaml
# GitHub配置
github:
  # 是否启用GitHub上传功能
  enabled: true
  # GitHub个人访问令牌（从环境变量获取）
  token: "${GITHUB_TOKEN}"
  # 仓库名称
  repo_name: "csxiefc/wx-mp-rss-merge"
  # 目标分支
  branch: "main"
  # 是否在生成JSON后自动上传
  auto_upload: true
```

## 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 测试GitHub连接

```bash
python test_github_upload.py
```

### 3. 启动服务

```bash
python run.py
```

### 4. 生成并上传文件

访问API接口：
```
GET http://localhost:8002/generate
```

## API响应格式

成功响应示例：

```json
{
  "code": 200,
  "msg": "成功",
  "fileUrl": "http://localhost:8002/files/result.json",
  "github": {
    "uploaded": true,
    "github_url": "https://github.com/csxiefc/wx-mp-rss-merge/blob/main/result.json",
    "repo": "csxiefc/wx-mp-rss-merge",
    "branch": "main"
  },
  "data": {
    "filename": "result.json",
    "record_count": 150,
    "recent_days": 3
  }
}
```

失败响应示例：

```json
{
  "code": 200,
  "msg": "成功",
  "fileUrl": "http://localhost:8002/files/result.json",
  "github": {
    "uploaded": false,
    "error": "GitHub上传失败"
  },
  "data": {
    "filename": "result.json",
    "record_count": 150,
    "recent_days": 3
  }
}
```

## 功能特性

### 1. 自动文件管理
- 如果文件不存在，创建新文件
- 如果文件已存在，自动更新替换
- 提交信息包含时间戳和操作类型

### 2. 错误处理
- 网络连接失败自动重试
- 权限不足时提供详细错误信息
- 令牌无效时给出明确提示

### 3. 安全特性
- 使用环境变量存储敏感信息
- 支持令牌权限验证
- 详细的日志记录

## 故障排除

### 1. 令牌相关错误

**错误**: `401 Unauthorized`
**解决**: 检查GitHub令牌是否正确，是否有足够的权限

**错误**: `403 Forbidden`
**解决**: 确保令牌有`repo`权限

### 2. 网络连接错误

**错误**: `Connection timeout`
**解决**: 检查网络连接，可能需要配置代理

### 3. 仓库权限错误

**错误**: `Repository not found`
**解决**: 检查仓库名称是否正确，确保有访问权限

### 4. 分支错误

**错误**: `Branch not found`
**解决**: 检查分支名称，确保分支存在

## 环境变量说明

| 变量名 | 说明 | 必需 | 示例 |
|--------|------|------|------|
| GITHUB_TOKEN | GitHub个人访问令牌 | 是 | `ghp_xxxxxxxxxxxx` |
| ENVIRONMENT | 运行环境 | 否 | `development` 或 `production` |

## 安全建议

1. **令牌安全**
   - 不要在代码中硬编码令牌
   - 定期轮换令牌
   - 使用最小权限原则

2. **环境隔离**
   - 开发和生产环境使用不同的令牌
   - 使用不同的仓库分支进行测试

3. **日志管理**
   - 定期检查上传日志
   - 监控异常上传行为

## 高级配置

### 自定义提交信息

可以在 `src/utils/github_uploader.py` 中修改提交信息格式：

```python
commit_message = f"更新 {filename} - 自动同步 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
```

### 禁用自动上传

在配置文件中设置：

```yaml
github:
  enabled: true
  auto_upload: false  # 禁用自动上传
```

### 使用不同分支

```yaml
github:
  branch: "develop"  # 使用develop分支
```

## 监控和日志

### 查看上传日志

```bash
# 查看应用日志
tail -f app.log

# 查看特定上传记录
grep "GitHub" app.log
```

### 检查文件状态

访问GitHub仓库查看文件是否成功上传：
```
https://github.com/csxiefc/wx-mp-rss-merge/blob/main/result.json
```

## 注意事项

1. **文件大小限制**: GitHub对单个文件有100MB的限制
2. **API限制**: GitHub API有速率限制，避免频繁上传
3. **网络稳定性**: 确保网络连接稳定，避免上传失败
4. **备份策略**: 建议保留本地文件备份

## 技术支持

如果遇到问题，请检查：

1. 环境变量是否正确设置
2. GitHub令牌是否有效
3. 网络连接是否正常
4. 仓库权限是否正确

更多帮助请参考GitHub API文档：https://docs.github.com/en/rest 