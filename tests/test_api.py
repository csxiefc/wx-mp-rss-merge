#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API接口测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import requests
import json
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 服务配置
BASE_URL = "http://106.13.63.117:8002"

def test_health_check():
    """测试健康检查接口"""
    logger.info("测试健康检查接口...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"健康检查成功: {data}")
            return True
        else:
            logger.error(f"健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"健康检查异常: {e}")
        return False

def test_index():
    """测试首页接口"""
    logger.info("测试首页接口...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"首页访问成功: {data}")
            return True
        else:
            logger.error(f"首页访问失败: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"首页访问异常: {e}")
        return False

def test_generate_json():
    """测试生成JSON文件接口"""
    logger.info("测试生成JSON文件接口...")
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/generate")
        end_time = time.time()
        
        logger.info(f"请求耗时: {end_time - start_time:.2f}秒")
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"生成JSON文件成功: {data}")
            
            # 验证返回数据格式
            if 'code' in data and 'msg' in data and 'fileUrl' in data:
                if data['code'] == 200:
                    logger.info("返回数据格式正确")
                    return data.get('fileUrl', '')
                else:
                    logger.error(f"生成失败: {data['msg']}")
                    return None
            else:
                logger.error("返回数据格式不正确")
                return None
        else:
            logger.error(f"生成JSON文件失败: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"生成JSON文件异常: {e}")
        return None

def test_download_file(file_url):
    """测试文件下载接口"""
    if not file_url:
        logger.error("文件URL为空，跳过下载测试")
        return False
    
    logger.info(f"测试文件下载接口: {file_url}")
    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            # 尝试解析JSON内容
            try:
                json_data = response.json()
                logger.info(f"文件下载成功，包含 {len(json_data)} 条记录")
                
                # 验证JSON格式
                if isinstance(json_data, list) and len(json_data) > 0:
                    first_item = json_data[0]
                    required_fields = ['mp_id', 'mp_name', 'mp_intro', 'title', 'url', 'content', 'description', 'publish_time']
                    
                    missing_fields = [field for field in required_fields if field not in first_item]
                    if missing_fields:
                        logger.error(f"JSON数据缺少字段: {missing_fields}")
                        return False
                    else:
                        logger.info("JSON数据格式正确")
                        return True
                else:
                    logger.error("JSON数据格式不正确或为空")
                    return False
            except json.JSONDecodeError as e:
                logger.error(f"JSON解析失败: {e}")
                return False
        else:
            logger.error(f"文件下载失败: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"文件下载异常: {e}")
        return False

def main():
    """主测试函数"""
    logger.info("=" * 50)
    logger.info("开始测试微信公众号RSS合并服务API")
    logger.info("=" * 50)
    
    # 测试健康检查
    if not test_health_check():
        logger.error("健康检查失败，服务可能未启动")
        return
    
    # 测试首页
    if not test_index():
        logger.error("首页访问失败")
        return
    
    # 测试生成JSON文件
    file_url = test_generate_json()
    if not file_url:
        logger.error("生成JSON文件失败")
        return
    
    # 测试文件下载
    if not test_download_file(file_url):
        logger.error("文件下载测试失败")
        return
    
    logger.info("=" * 50)
    logger.info("所有API测试通过！")
    logger.info("=" * 50)

if __name__ == '__main__':
    main() 