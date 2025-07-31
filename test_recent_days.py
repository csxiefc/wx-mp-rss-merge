#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试recent_days逻辑
"""

import os
import sys
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import DatabaseManager
from src.utils.config import load_config

def test_recent_days_logic():
    """测试recent_days逻辑"""
    print("=== 测试recent_days逻辑 ===")
    
    try:
        # 加载配置
        config = load_config()
        recent_days = config['data']['recent_days']
        
        print(f"配置的recent_days: {recent_days}")
        
        # 测试时间计算逻辑
        end_time = datetime.now()
        
        if recent_days == 0:
            # 获取当天的开始时间（00:00:00）
            start_time = end_time.replace(hour=0, minute=0, second=0, microsecond=0)
            print(f"获取当天数据: {start_time.strftime('%Y-%m-%d %H:%M:%S')} 到 {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            # 获取最近几天的数据
            start_time = end_time - timedelta(days=recent_days)
            print(f"获取最近{recent_days}天数据: {start_time.strftime('%Y-%m-%d %H:%M:%S')} 到 {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 转换为时间戳
        start_timestamp = int(start_time.timestamp())
        end_timestamp = int(end_time.timestamp())
        
        print(f"时间戳范围: {start_timestamp} 到 {end_timestamp}")
        
        # 测试数据库连接和数据获取
        print("\n=== 测试数据库连接 ===")
        with DatabaseManager() as db:
            # 获取所有feeds
            feeds = db.get_all_feeds()
            print(f"获取到 {len(feeds)} 个公众号")
            
            if feeds:
                # 测试第一个公众号的数据获取
                first_feed = feeds[0]
                mp_id = first_feed['id']
                mp_name = first_feed.get('mp_name', mp_id)
                
                print(f"\n测试公众号: {mp_name} (ID: {mp_id})")
                articles = db.get_recent_articles(mp_id, recent_days)
                print(f"获取到 {len(articles)} 篇文章")
                
                if articles:
                    print("文章列表:")
                    for i, article in enumerate(articles[:3]):  # 只显示前3篇
                        publish_time = datetime.fromtimestamp(article['publish_time'])
                        print(f"  {i+1}. {article['title']} - {publish_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    if len(articles) > 3:
                        print(f"  ... 还有 {len(articles) - 3} 篇文章")
                else:
                    print("  没有找到符合条件的文章")
        
        print("\n✅ 测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("recent_days逻辑测试")
    print("=" * 50)
    
    success = test_recent_days_logic()
    
    if success:
        print("\n🎉 测试通过！")
        print("\n📋 说明:")
        print("- recent_days = 0: 获取当天的数据（从00:00:00开始）")
        print("- recent_days = 1: 获取最近1天的数据")
        print("- recent_days = 3: 获取最近3天的数据")
    else:
        print("\n❌ 测试失败！")
        sys.exit(1)

if __name__ == "__main__":
    main() 