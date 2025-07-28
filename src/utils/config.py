#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置管理模块
"""

import os
import yaml
import logging

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
            config = yaml.safe_load(file)
        
        # 根据环境自动设置URL前缀
        config = _set_url_prefix(config)
        
        return config
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        raise

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