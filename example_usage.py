#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub上传功能使用示例
"""

import os
import sys
import requests
import json

def test_generate_and_upload():
    """测试生成JSON并上传到GitHub"""
    
    print("=== GitHub上传功能测试 ===")
    
    # 检查环境变量
    if not os.getenv('GITHUB_TOKEN'):
        print("❌ 错误: 请先设置GITHUB_TOKEN环境变量")
        print("设置方法:")
        print("Windows: set GITHUB_TOKEN=your_token")
        print("Linux/Mac: export GITHUB_TOKEN=your_token")
        return False
    
    # 测试服务是否运行
    try:
        response = requests.get('http://localhost:8002/health', timeout=5)
        if response.status_code != 200:
            print("❌ 错误: 服务未运行，请先启动服务")
            print("启动命令: python run.py")
            return False
        print("✅ 服务运行正常")
    except requests.exceptions.RequestException:
        print("❌ 错误: 无法连接到服务，请确保服务正在运行")
        print("启动命令: python run.py")
        return False
    
    # 调用生成接口
    print("\n正在生成JSON文件并上传到GitHub...")
    try:
        response = requests.get('http://localhost:8002/generate', timeout=30)
        result = response.json()
        
        if result['code'] == 200:
            print("✅ JSON文件生成成功")
            print(f"📁 文件名: {result['data']['filename']}")
            print(f"📊 记录数: {result['data']['record_count']}")
            print(f"🔗 本地URL: {result['fileUrl']}")
            
            # 检查GitHub上传状态
            github_info = result.get('github', {})
            if github_info.get('uploaded'):
                print("✅ GitHub上传成功")
                print(f"🌐 GitHub URL: {github_info['github_url']}")
                print(f"📦 仓库: {github_info['repo']}")
                print(f"🌿 分支: {github_info['branch']}")
                if github_info.get('upload_path'):
                    print(f"📂 上传目录: {github_info['upload_path']}")
                else:
                    print("📂 上传目录: 根目录")
            else:
                print("❌ GitHub上传失败")
                if 'error' in github_info:
                    print(f"错误信息: {github_info['error']}")
                elif 'reason' in github_info:
                    print(f"原因: {github_info['reason']}")
            
            return True
        else:
            print(f"❌ 生成失败: {result['msg']}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ 响应解析失败: {e}")
        return False

def test_download_file():
    """测试下载文件"""
    print("\n=== 测试文件下载 ===")
    
    try:
        response = requests.get('http://localhost:8002/files/result.json', timeout=10)
        if response.status_code == 200:
            print("✅ 文件下载成功")
            print(f"📄 文件大小: {len(response.content)} 字节")
            
            # 解析JSON内容
            try:
                data = response.json()
                print(f"📊 JSON记录数: {len(data)}")
                if data:
                    print(f"📝 第一条记录标题: {data[0].get('title', 'N/A')}")
            except json.JSONDecodeError:
                print("⚠️ 文件内容不是有效的JSON格式")
            
            return True
        else:
            print(f"❌ 文件下载失败: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 下载请求失败: {e}")
        return False

def main():
    """主函数"""
    print("微信公众号RSS合并服务 - GitHub上传功能测试")
    print("=" * 50)
    
    # 测试生成和上传
    if test_generate_and_upload():
        # 测试下载
        test_download_file()
        
        print("\n🎉 所有测试完成！")
        print("\n📋 使用说明:")
        print("1. 确保设置了GITHUB_TOKEN环境变量")
        print("2. 启动服务: python run.py")
        print("3. 访问: http://localhost:8002/generate")
        print("4. 查看GitHub仓库: https://github.com/csxiefc/wx-mp-rss-merge")
        print("5. 文件将上传到: testres/result.json")
    else:
        print("\n❌ 测试失败，请检查配置和网络连接")

if __name__ == "__main__":
    main() 