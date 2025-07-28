#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据库连接测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.core.database import DatabaseManager
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection():
    """测试数据库连接"""
    try:
        logger.info("开始测试数据库连接...")
        
        with DatabaseManager() as db:
            # 测试获取feeds数据
            feeds = db.get_all_feeds()
            logger.info(f"成功获取 {len(feeds)} 个公众号")
            
            if feeds:
                # 测试获取第一个公众号的文章
                first_feed = feeds[0]
                mp_id = first_feed['id']
                mp_name = first_feed.get('mp_name', mp_id)
                
                logger.info(f"测试获取公众号 '{mp_name}' 的文章...")
                articles = db.get_recent_articles(mp_id, 3)
                logger.info(f"成功获取 {len(articles)} 篇文章")
                
                # 显示一些示例数据
                if articles:
                    first_article = articles[0]
                    logger.info(f"示例文章: {first_article.get('title', '无标题')}")
                
            logger.info("数据库连接测试成功！")
            return True
            
    except Exception as e:
        logger.error(f"数据库连接测试失败: {e}")
        return False

if __name__ == '__main__':
    test_database_connection() 