#!/bin/bash

# 微信公众号RSS合并服务 - 基于现有环境的部署脚本
# 使用方法: ./scripts/deploy-with-existing.sh [start|stop|restart|logs|status]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$PROJECT_ROOT/docker-compose.yml"

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Docker是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker未安装，请先安装Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose未安装，请先安装Docker Compose"
        exit 1
    fi
    
    log_info "Docker环境检查通过"
}

# 检查网络是否存在
check_network() {
    log_info "检查werss-net网络..."
    
    if ! docker network ls | grep -q "werss-net"; then
        log_error "werss-net网络不存在，请先创建网络"
        log_info "创建网络命令: docker network create werss-net"
        exit 1
    fi
    
    log_info "werss-net网络检查通过"
}

# 检查现有服务
check_existing_services() {
    log_info "检查现有服务..."
    
    # 检查MySQL8服务
    if docker ps --format "table {{.Names}}" | grep -q "mysql8"; then
        log_info "MySQL8服务正在运行"
    else
        log_warn "MySQL8服务未运行，将启动新的MySQL8容器"
    fi
    
    # 检查we-mp-rss服务
    if docker ps --format "table {{.Names}}" | grep -q "we-mp-rss"; then
        log_warn "发现现有的we-mp-rss服务，建议停止后重新部署"
    fi
}

# 创建必要的目录
create_directories() {
    log_info "创建必要的目录..."
    
    mkdir -p "$PROJECT_ROOT/storage"
    mkdir -p "$PROJECT_ROOT/logs"
    mkdir -p "$PROJECT_ROOT/nginx/ssl"
    
    # 设置权限
    chmod 755 "$PROJECT_ROOT/storage"
    chmod 755 "$PROJECT_ROOT/logs"
    
    log_info "目录创建完成"
}

# 启动服务
start_service() {
    log_info "启动微信公众号RSS合并服务..."
    
    cd "$PROJECT_ROOT"
    
    # 构建镜像
    log_info "构建Docker镜像..."
    docker-compose build --no-cache
    
    # 启动服务
    log_info "启动Docker容器..."
    docker-compose up -d
    
    # 等待服务启动
    log_info "等待服务启动..."
    sleep 30
    
    # 检查服务状态
    check_service_status
    
    log_info "服务启动完成！"
    log_info "访问地址: http://localhost:8002"
    log_info "API文档: http://localhost:8002/health"
}

# 停止服务
stop_service() {
    log_info "停止微信公众号RSS合并服务..."
    
    cd "$PROJECT_ROOT"
    docker-compose down
    
    log_info "服务已停止"
}

# 重启服务
restart_service() {
    log_info "重启微信公众号RSS合并服务..."
    
    stop_service
    sleep 5
    start_service
}

# 查看日志
show_logs() {
    log_info "显示服务日志..."
    
    cd "$PROJECT_ROOT"
    docker-compose logs -f
}

# 查看状态
show_status() {
    log_info "检查服务状态..."
    
    cd "$PROJECT_ROOT"
    
    # 显示容器状态
    docker-compose ps
    
    # 检查健康状态
    if curl -s http://localhost:8002/health > /dev/null; then
        log_info "服务运行正常"
    else
        log_warn "服务可能存在问题，请检查日志"
    fi
    
    # 显示网络信息
    log_info "网络信息:"
    docker network ls | grep werss-net
}

# 检查服务状态
check_service_status() {
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:8002/health > /dev/null 2>&1; then
            log_info "服务已就绪"
            return 0
        fi
        
        log_info "等待服务启动... (${attempt}/${max_attempts})"
        sleep 10
        attempt=$((attempt + 1))
    done
    
    log_error "服务启动超时，请检查日志"
    return 1
}

# 清理
cleanup() {
    log_info "清理Docker资源..."
    
    cd "$PROJECT_ROOT"
    
    # 停止并删除容器
    docker-compose down -v
    
    # 删除未使用的镜像
    docker image prune -f
    
    log_info "清理完成"
}

# 备份数据
backup_data() {
    log_info "备份数据..."
    
    local backup_dir="$PROJECT_ROOT/backup/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # 备份MySQL数据
    docker exec mysql8 mysqldump -u root -pStrongPass123! wewe-rss > "$backup_dir/database.sql"
    
    # 备份存储文件
    cp -r "$PROJECT_ROOT/storage" "$backup_dir/"
    
    log_info "备份完成: $backup_dir"
}

# 连接到现有网络
connect_to_network() {
    log_info "连接到werss-net网络..."
    
    # 检查当前容器是否在正确的网络中
    if ! docker inspect wx-mp-rss-service 2>/dev/null | grep -q "werss-net"; then
        log_info "将容器连接到werss-net网络"
        docker network connect werss-net wx-mp-rss-service 2>/dev/null || true
    fi
    
    log_info "网络连接检查完成"
}

# 显示网络信息
show_network_info() {
    log_info "显示网络信息..."
    
    echo "=== 网络列表 ==="
    docker network ls
    
    echo ""
    echo "=== werss-net网络详情 ==="
    docker network inspect werss-net
    
    echo ""
    echo "=== 容器网络连接 ==="
    docker ps --format "table {{.Names}}\t{{.Networks}}"
}

# 主函数
main() {
    case "${1:-start}" in
        start)
            check_docker
            check_network
            check_existing_services
            create_directories
            start_service
            connect_to_network
            ;;
        stop)
            stop_service
            ;;
        restart)
            restart_service
            ;;
        logs)
            show_logs
            ;;
        status)
            show_status
            ;;
        network)
            show_network_info
            ;;
        cleanup)
            cleanup
            ;;
        backup)
            backup_data
            ;;
        *)
            echo "使用方法: $0 {start|stop|restart|logs|status|network|cleanup|backup}"
            echo ""
            echo "命令说明:"
            echo "  start   - 启动服务"
            echo "  stop    - 停止服务"
            echo "  restart - 重启服务"
            echo "  logs    - 查看日志"
            echo "  status  - 查看状态"
            echo "  network - 显示网络信息"
            echo "  cleanup - 清理资源"
            echo "  backup  - 备份数据"
            echo ""
            echo "注意事项:"
            echo "  - 此脚本使用现有的werss-net网络"
            echo "  - 确保MySQL8服务已正确配置"
            echo "  - 端口8002用于API访问"
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@" 