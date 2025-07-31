#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置管理模块
"""

import os
import yaml
import logging
import re

logger = logging.getLogger(__name__)

def get_config_path():
    """获取配置文件路径"""
    # 获取项目根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    return config_path

def load_config():
    """加载配置文件"""
    try:
        config_path = get_config_path()
        with open(config_path, 'r', encoding='utf-8') as file:
            config_content = file.read()
        
        # 替换环境变量
        config_content = _replace_env_vars(config_content)
        
        # 解析YAML
        config = yaml.safe_load(config_content)
        
        # 根据环境自动设置URL前缀
        config = _set_url_prefix(config)
        
        return config
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        raise

def _replace_env_vars(content):
    """
    替换配置文件中的环境变量
    
    Args:
        content: 配置文件内容
        
    Returns:
        str: 替换后的内容
    """
    # 匹配 ${VAR_NAME} 格式的环境变量
    pattern = r'\$\{([^}]+)\}'
    
    def replace_var(match):
        var_name = match.group(1)
        var_value = os.getenv(var_name)
        if var_value is None:
            logger.warning(f"环境变量 {var_name} 未设置，使用空字符串")
            return '""'
        return var_value
    
    return re.sub(pattern, replace_var, content)

def _set_url_prefix(config):
    """根据环境设置URL前缀"""
    try:
        # 检查环境变量
        env = os.getenv('ENVIRONMENT', 'development').lower()
        
        if env == 'production':
            # 生产环境使用服务器IP
            config['file']['url_prefix'] = config['file']['url_prefix_prod']
            logger.info("使用生产环境配置: 服务器IP")
        else:
            # 开发环境使用localhost
            config['file']['url_prefix'] = config['file']['url_prefix_dev']
            logger.info("使用开发环境配置: localhost")
        
        return config
    except Exception as e:
        logger.warning(f"设置URL前缀失败，使用默认配置: {e}")
        # 如果配置中没有环境相关的前缀，使用默认值
        if 'url_prefix' not in config['file']:
            config['file']['url_prefix'] = "http://localhost:8002/files"
        return config 