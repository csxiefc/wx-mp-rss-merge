#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
集成测试脚本 - 验证整个数据生成流程
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import json
import logging
from src.core.database import DatabaseManager
from src.core.data_processor import DataProcessor
from src.utils.file_manager import FileManager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_full_workflow():
    """测试完整的工作流程"""
    try:
        logger.info("开始测试完整工作流程...")
        
        # 1. 初始化组件
        file_manager = FileManager()
        data_processor = DataProcessor(recent_days=3)
        
        # 2. 获取数据
        with DatabaseManager() as db:
            # 获取所有feeds
            feeds = db.get_all_feeds()
            logger.info(f"获取到 {len(feeds)} 个公众号")
            
            all_articles = []
            # 循环获取每个公众号的文章
            for feed in feeds:
                mp_id = feed['id']
                articles = db.get_recent_articles(mp_id, 3)
                logger.info(f"公众号 {feed.get('mp_name', mp_id)} 获取到 {len(articles)} 篇文章")
                all_articles.extend(articles)
            
            # 3. 处理数据
            processed_data = data_processor.process_data(feeds, all_articles)
            logger.info(f"处理完成，共生成 {len(processed_data)} 条记录")
            
            # 4. 保存JSON文件
            filename = file_manager.save_json_file(processed_data)
            file_url = file_manager.get_file_url(filename)
            
            logger.info(f"JSON文件保存成功: {filename}")
            logger.info(f"文件访问URL: {file_url}")
            
            # 5. 显示示例数据
            if processed_data:
                example = processed_data[0]
                logger.info("示例数据:")
                logger.info(f"  公众号: {example.get('mp_name', 'N/A')}")
                logger.info(f"  文章标题: {example.get('title', 'N/A')}")
                logger.info(f"  发布时间: {example.get('publish_time', 'N/A')}")
            
            return {
                "success": True,
                "filename": filename,
                "file_url": file_url,
                "record_count": len(processed_data)
            }
            
    except Exception as e:
        logger.error(f"测试失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == '__main__':
    result = test_full_workflow()
    if result["success"]:
        logger.info("=" * 50)
        logger.info("测试成功完成！")
        logger.info(f"生成文件: {result['filename']}")
        logger.info(f"文件URL: {result['file_url']}")
        logger.info(f"记录数量: {result['record_count']}")
        logger.info("=" * 50)
    else:
        logger.error(f"测试失败: {result['error']}") 