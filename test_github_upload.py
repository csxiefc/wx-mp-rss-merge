#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub上传功能测试脚本
"""

import os
import sys
import json
import logging

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.github_uploader import GitHubUploader
from src.utils.config import load_config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_github_upload():
    """测试GitHub上传功能"""
    try:
        # 加载配置
        config = load_config()
        github_config = config.get('github', {})
        
        if not github_config.get('enabled', False):
            logger.warning("GitHub功能未启用，请检查配置文件")
            return False
        
        # 检查GitHub令牌
        token = github_config.get('token')
        if not token:
            logger.error("GitHub令牌未设置，请设置GITHUB_TOKEN环境变量")
            return False
        
        # 创建测试文件
        test_data = {
            "test": "data",
            "timestamp": "2024-01-01 00:00:00",
            "message": "这是一个测试文件",
            "upload_path": github_config.get('upload_path', '')
        }
        
        test_file_path = "test_result.json"
        with open(test_file_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"创建测试文件: {test_file_path}")
        
        # 初始化GitHub上传器
        github_uploader = GitHubUploader(
            token=token,
            repo_name=github_config['repo_name']
        )
        
        # 测试连接
        if not github_uploader.connect():
            logger.error("无法连接到GitHub")
            return False
        
        # 获取上传路径
        upload_path = github_config.get('upload_path', '')
        if upload_path:
            logger.info(f"上传到目录: {upload_path}")
        else:
            logger.info("上传到根目录")
        
        # 上传文件
        if github_uploader.upload_file(
            test_file_path, 
            github_config.get('branch', 'main'),
            upload_path
        ):
            logger.info("文件上传成功")
            
            # 获取文件URL
            file_url = github_uploader.get_file_url("test_result.json", upload_path)
            if file_url:
                logger.info(f"文件URL: {file_url}")
            
            # 清理测试文件
            os.remove(test_file_path)
            logger.info("测试文件已清理")
            
            github_uploader.close()
            return True
        else:
            logger.error("文件上传失败")
            return False
            
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}")
        return False

if __name__ == "__main__":
    print("开始测试GitHub上传功能...")
    
    # 检查环境变量
    if not os.getenv('GITHUB_TOKEN'):
        print("错误: 请设置GITHUB_TOKEN环境变量")
        print("设置方法:")
        print("Windows: set GITHUB_TOKEN=your_token")
        print("Linux/Mac: export GITHUB_TOKEN=your_token")
        sys.exit(1)
    
    success = test_github_upload()
    
    if success:
        print("✅ GitHub上传功能测试成功")
    else:
        print("❌ GitHub上传功能测试失败")
        sys.exit(1) 