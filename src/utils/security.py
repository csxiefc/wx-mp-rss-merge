#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
安全工具模块
"""

import time
import hashlib
import hmac
from functools import wraps
from flask import request, jsonify, g
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class SecurityManager:
    def __init__(self, config):
        """初始化安全管理器"""
        self.config = config
        self.security_config = config.get('security', {})
        self.rate_limit_data = defaultdict(list)
    
    def verify_api_key(self, api_key):
        """验证API密钥"""
        expected_key = self.security_config.get('api_key', '')
        return api_key == expected_key
    
    def check_ip_whitelist(self, client_ip):
        """检查IP白名单"""
        if not self.security_config.get('ip_whitelist_enabled', False):
            return True
        
        whitelist = self.security_config.get('ip_whitelist', [])
        return client_ip in whitelist
    
    def check_rate_limit(self, client_ip):
        """检查请求频率限制"""
        if not self.security_config.get('rate_limit_enabled', False):
            return True
        
        current_time = time.time()
        window = self.security_config.get('rate_limit_window', 60)
        max_requests = self.security_config.get('rate_limit_requests', 10)
        
        # 清理过期的请求记录
        self.rate_limit_data[client_ip] = [
            req_time for req_time in self.rate_limit_data[client_ip]
            if current_time - req_time < window
        ]
        
        # 检查请求次数
        if len(self.rate_limit_data[client_ip]) >= max_requests:
            return False
        
        # 添加当前请求
        self.rate_limit_data[client_ip].append(current_time)
        return True
    
    def get_client_ip(self):
        """获取客户端IP"""
        # 检查代理头
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        else:
            return request.remote_addr
    
    def log_security_event(self, event_type, details):
        """记录安全事件"""
        client_ip = self.get_client_ip()
        logger.warning(f"安全事件 - {event_type}: IP={client_ip}, 详情={details}")

def require_api_key(f):
    """API密钥认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from src.utils.config import load_config
        config = load_config()
        security_config = config.get('security', {})
        
        if not security_config.get('api_key_required', False):
            return f(*args, **kwargs)
        
        # 从请求头获取API密钥
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            return jsonify({
                "code": 401,
                "msg": "缺少API密钥",
                "error": "请在请求头中添加 X-API-Key 或使用 api_key 参数"
            }), 401
        
        # 验证API密钥
        security_manager = SecurityManager(config)
        if not security_manager.verify_api_key(api_key):
            security_manager.log_security_event("API密钥验证失败", f"提供的密钥: {api_key[:8]}...")
            return jsonify({
                "code": 401,
                "msg": "API密钥无效",
                "error": "请检查API密钥是否正确"
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function

def require_ip_whitelist(f):
    """IP白名单检查装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from src.utils.config import load_config
        config = load_config()
        security_manager = SecurityManager(config)
        
        client_ip = security_manager.get_client_ip()
        
        if not security_manager.check_ip_whitelist(client_ip):
            security_manager.log_security_event("IP白名单检查失败", f"客户端IP: {client_ip}")
            return jsonify({
                "code": 403,
                "msg": "IP地址未授权",
                "error": f"IP地址 {client_ip} 不在白名单中"
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

def rate_limit(f):
    """请求频率限制装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from src.utils.config import load_config
        config = load_config()
        security_manager = SecurityManager(config)
        
        client_ip = security_manager.get_client_ip()
        
        if not security_manager.check_rate_limit(client_ip):
            security_manager.log_security_event("请求频率超限", f"客户端IP: {client_ip}")
            return jsonify({
                "code": 429,
                "msg": "请求过于频繁",
                "error": "请稍后再试"
            }), 429
        
        return f(*args, **kwargs)
    return decorated_function

def validate_request(f):
    """请求验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查请求方法
        if request.method not in ['GET', 'POST']:
            return jsonify({
                "code": 405,
                "msg": "不支持的请求方法",
                "error": f"方法 {request.method} 不被允许"
            }), 405
        
        # 检查请求大小
        if request.content_length and request.content_length > 16777216:  # 16MB
            return jsonify({
                "code": 413,
                "msg": "请求体过大",
                "error": "请求体大小不能超过16MB"
            }), 413
        
        return f(*args, **kwargs)
    return decorated_function

def log_request(f):
    """请求日志装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        
        # 记录请求信息
        logger.info(f"收到请求: {request.method} {request.path} - IP: {request.remote_addr}")
        
        # 执行请求
        response = f(*args, **kwargs)
        
        # 记录响应时间
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"请求完成: {request.method} {request.path} - 耗时: {duration:.3f}秒")
        
        return response
    return decorated_function 