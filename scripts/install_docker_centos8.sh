#!/bin/bash

# CentOS 8 Docker安装脚本
# 使用方法: ./scripts/install_docker_centos8.sh

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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

# 检查是否为root用户
check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "此脚本需要root权限运行"
        log_error "请使用: sudo $0"
        exit 1
    fi
}

# 检查系统版本
check_system() {
    if ! grep -q "CentOS Linux release 8" /etc/redhat-release; then
        log_warn "此脚本专为CentOS 8设计，当前系统可能不兼容"
    fi
    
    log_info "系统检查完成"
}

# 更新系统
update_system() {
    log_info "更新系统包..."
    
    dnf update -y
    
    log_info "系统更新完成"
}

# 安装必要的包
install_packages() {
    log_info "安装必要的系统包..."
    
    dnf install -y \
        yum-utils \
        device-mapper-persistent-data \
        lvm2 \
        curl \
        wget \
        git
    
    log_info "系统包安装完成"
}

# 添加Docker仓库
add_docker_repo() {
    log_info "添加Docker官方仓库..."
    
    dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    
    log_info "Docker仓库添加完成"
}

# 安装Docker
install_docker() {
    log_info "安装Docker..."
    
    dnf install -y docker-ce docker-ce-cli containerd.io
    
    # 启动Docker服务
    systemctl start docker
    systemctl enable docker
    
    log_info "Docker安装完成"
}

# 安装Docker Compose
install_docker_compose() {
    log_info "安装Docker Compose..."
    
    # 下载最新版本的Docker Compose
    COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
    
    curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    
    chmod +x /usr/local/bin/docker-compose
    
    # 创建软链接
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
    
    log_info "Docker Compose安装完成"
}

# 配置Docker
configure_docker() {
    log_info "配置Docker..."
    
    # 创建docker用户组
    groupadd docker 2>/dev/null || true
    
    # 将当前用户添加到docker组
    if [[ -n "$SUDO_USER" ]]; then
        usermod -aG docker "$SUDO_USER"
        log_info "已将用户 $SUDO_USER 添加到docker组"
    fi
    
    # 配置Docker守护进程
    mkdir -p /etc/docker
    cat > /etc/docker/daemon.json << EOF
{
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "10m",
        "max-file": "3"
    },
    "storage-driver": "overlay2",
    "storage-opts": [
        "overlay2.override_kernel_check=true"
    ]
}
EOF
    
    # 重启Docker服务
    systemctl restart docker
    
    log_info "Docker配置完成"
}

# 配置防火墙
configure_firewall() {
    log_info "配置防火墙..."
    
    # 安装firewalld（如果未安装）
    dnf install -y firewalld
    
    # 启动firewalld
    systemctl start firewalld
    systemctl enable firewalld
    
    # 开放必要的端口
    firewall-cmd --permanent --add-port=80/tcp
    firewall-cmd --permanent --add-port=443/tcp
    firewall-cmd --permanent --add-port=8002/tcp
    firewall-cmd --permanent --add-port=3306/tcp
    
    # 重新加载防火墙规则
    firewall-cmd --reload
    
    log_info "防火墙配置完成"
}

# 配置SELinux
configure_selinux() {
    log_info "配置SELinux..."
    
    # 检查SELinux状态
    if command -v sestatus &> /dev/null; then
        SELINUX_STATUS=$(sestatus | grep "SELinux status" | awk '{print $3}')
        
        if [[ "$SELINUX_STATUS" == "enabled" ]]; then
            log_warn "SELinux已启用，建议配置Docker与SELinux的兼容性"
            
            # 安装SELinux策略
            dnf install -y container-selinux
            
            # 重启Docker服务
            systemctl restart docker
            
            log_info "SELinux配置完成"
        else
            log_info "SELinux已禁用"
        fi
    else
        log_info "SELinux未安装"
    fi
}

# 验证安装
verify_installation() {
    log_info "验证Docker安装..."
    
    # 检查Docker版本
    if docker --version; then
        log_info "Docker安装成功"
    else
        log_error "Docker安装失败"
        exit 1
    fi
    
    # 检查Docker Compose版本
    if docker-compose --version; then
        log_info "Docker Compose安装成功"
    else
        log_error "Docker Compose安装失败"
        exit 1
    fi
    
    # 测试Docker
    if docker run hello-world; then
        log_info "Docker测试成功"
    else
        log_error "Docker测试失败"
        exit 1
    fi
}

# 显示使用说明
show_usage() {
    log_info "Docker安装完成！"
    echo ""
    echo "使用说明:"
    echo "1. 重新登录以应用docker组权限，或运行: newgrp docker"
    echo "2. 启动服务: ./scripts/deploy.sh start"
    echo "3. 查看状态: ./scripts/deploy.sh status"
    echo "4. 查看日志: ./scripts/deploy.sh logs"
    echo "5. 停止服务: ./scripts/deploy.sh stop"
    echo ""
    echo "常用Docker命令:"
    echo "  docker ps                    # 查看运行中的容器"
    echo "  docker images               # 查看镜像"
    echo "  docker logs <container>    # 查看容器日志"
    echo "  docker exec -it <container> bash  # 进入容器"
    echo ""
}

# 主函数
main() {
    log_info "开始安装Docker环境..."
    
    check_root
    check_system
    update_system
    install_packages
    add_docker_repo
    install_docker
    install_docker_compose
    configure_docker
    configure_firewall
    configure_selinux
    verify_installation
    show_usage
    
    log_info "Docker环境安装完成！"
}

# 执行主函数
main "$@" 