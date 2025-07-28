#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
安全功能测试脚本
"""

import sys
import os
import requests
import json
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(__file__))

def test_api_access():
    """测试API访问"""
    print("1. 测试API访问...")
    
    # 测试直接访问（无需API密钥）
    print("   测试直接访问...")
    response = requests.get("http://localhost:8002/generate")
    if response.status_code == 200:
        print("   ✓ 可以直接访问API")
        return True
    else:
        print(f"   ✗ 错误: 应该返回200，实际返回{response.status_code}")
        return False

def test_rate_limiting():
    """测试请求频率限制"""
    print("\n2. 测试请求频率限制...")
    
    headers = {"X-API-Key": "your-secret-api-key-2024"}
    
    # 发送多个请求测试频率限制
    print("   发送多个请求测试频率限制...")
    for i in range(12):  # 超过限制的10次
        response = requests.get("http://localhost:8002/generate")
        print(f"   请求 {i+1}: {response.status_code}")
        
        if response.status_code == 429:
            print("   ✓ 正确触发频率限制")
            return True
    
    print("   ✗ 错误: 没有触发频率限制")
    return False

def test_request_validation():
    """测试请求验证"""
    print("\n3. 测试请求验证...")
    
    # 测试不支持的请求方法
    print("   测试不支持的请求方法...")
    response = requests.post("http://localhost:8002/generate")
    if response.status_code == 405:
        print("   ✓ 正确拒绝不支持的请求方法")
    else:
        print(f"   ✗ 错误: 应该返回405，实际返回{response.status_code}")
        return False
    
    # 测试健康检查接口（无需API密钥）
    print("   测试健康检查接口...")
    response = requests.get("http://localhost:8002/health")
    if response.status_code == 200:
        print("   ✓ 健康检查接口正常工作")
        return True
    else:
        print(f"   ✗ 错误: 健康检查应该返回200，实际返回{response.status_code}")
        return False

def test_file_download_security():
    """测试文件下载安全"""
    print("\n4. 测试文件下载安全...")
    
    # 测试下载不存在的文件
    print("   测试下载不存在的文件...")
    response = requests.get("http://localhost:8002/files/nonexistent.json")
    if response.status_code == 404:
        print("   ✓ 正确拒绝不存在的文件")
    else:
        print(f"   ✗ 错误: 应该返回404，实际返回{response.status_code}")
        return False
    
    # 测试下载存在的文件（需要先生成）
    print("   测试下载存在的文件...")
    response = requests.get("http://localhost:8002/generate")
    if response.status_code == 200:
        data = response.json()
        file_url = data['fileUrl']
        
        download_response = requests.get(file_url)
        if download_response.status_code == 200:
            print("   ✓ 文件下载正常工作")
            return True
        else:
            print(f"   ✗ 错误: 文件下载失败，状态码{download_response.status_code}")
            return False
    else:
        print(f"   ✗ 错误: 生成文件失败，状态码{response.status_code}")
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n5. 测试错误处理...")
    
    # 测试不存在的接口
    print("   测试不存在的接口...")
    response = requests.get("http://localhost:8002/nonexistent")
    if response.status_code == 404:
        data = response.json()
        if data.get('code') == 404:
            print("   ✓ 正确处理404错误")
            return True
        else:
            print("   ✗ 错误: 404响应格式不正确")
            return False
    else:
        print(f"   ✗ 错误: 应该返回404，实际返回{response.status_code}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("安全功能测试")
    print("=" * 50)
    
    # 等待服务启动
    print("等待服务启动...")
    time.sleep(2)
    
    # 运行测试
    tests = [
        test_api_access,
        test_rate_limiting,
        test_request_validation,
        test_file_download_security,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"   ✗ 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有安全测试通过！")
    else:
        print("✗ 部分安全测试失败！") 