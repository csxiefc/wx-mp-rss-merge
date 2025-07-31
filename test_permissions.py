#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
权限测试脚本
"""

import os
import sys
import json
import tempfile

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.file_manager import FileManager

def test_file_permissions():
    """测试文件权限"""
    print("=== 文件权限测试 ===")
    
    try:
        # 初始化文件管理器
        file_manager = FileManager()
        
        print(f"存储路径: {file_manager.storage_path}")
        print(f"存储路径是否存在: {os.path.exists(file_manager.storage_path)}")
        
        # 测试写入权限
        test_data = [
            {"test": "data", "timestamp": "2024-01-01 00:00:00"}
        ]
        
        filename = file_manager.save_json_file(test_data)
        print(f"✅ 文件写入成功: {filename}")
        
        # 检查文件是否存在
        file_path = os.path.join(file_manager.storage_path, filename)
        print(f"文件路径: {file_path}")
        print(f"文件是否存在: {os.path.exists(file_path)}")
        
        # 检查文件权限
        if os.path.exists(file_path):
            stat = os.stat(file_path)
            print(f"文件权限: {oct(stat.st_mode)}")
            print(f"文件大小: {stat.st_size} 字节")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_directory_permissions():
    """测试目录权限"""
    print("\n=== 目录权限测试 ===")
    
    try:
        # 检查当前工作目录
        cwd = os.getcwd()
        print(f"当前工作目录: {cwd}")
        
        # 检查storage目录
        storage_path = os.path.join(cwd, "storage")
        print(f"Storage目录: {storage_path}")
        print(f"Storage目录是否存在: {os.path.exists(storage_path)}")
        
        if os.path.exists(storage_path):
            stat = os.stat(storage_path)
            print(f"Storage目录权限: {oct(stat.st_mode)}")
        
        # 尝试创建测试目录
        test_dir = os.path.join(cwd, "test_dir")
        os.makedirs(test_dir, exist_ok=True)
        print(f"✅ 测试目录创建成功: {test_dir}")
        
        # 清理测试目录
        os.rmdir(test_dir)
        print("✅ 测试目录清理成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 目录测试失败: {e}")
        return False

def main():
    """主函数"""
    print("文件权限测试")
    print("=" * 50)
    
    # 测试目录权限
    dir_success = test_directory_permissions()
    
    # 测试文件权限
    file_success = test_file_permissions()
    
    if dir_success and file_success:
        print("\n🎉 所有测试通过！")
    else:
        print("\n❌ 部分测试失败！")
        sys.exit(1)

if __name__ == "__main__":
    main() 