#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
微信公众号RSS合并服务启动脚本
"""

import os
import sys
import logging
from src.api.app import create_app, load_config

def setup_logging():
    """设置日志配置"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log', encoding='utf-8')
        ]
    )

def main():
    """主函数"""
    try:
        # 设置日志
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # 加载配置
        config = load_config()
        app_config = config['app']
        
        logger.info("=" * 50)
        logger.info("微信公众号RSS合并服务启动中...")
        logger.info(f"服务地址: http://{app_config['host']}:{app_config['port']}")
        logger.info(f"调试模式: {app_config['debug']}")
        logger.info("=" * 50)
        
        # 创建并启动应用
        app = create_app()
        app.run(
            host=app_config['host'],
            port=app_config['port'],
            debug=app_config['debug']
        )
        
    except KeyboardInterrupt:
        logger.info("服务被用户中断")
    except Exception as e:
        logger.error(f"服务启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 