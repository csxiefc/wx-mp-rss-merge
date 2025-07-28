import json
import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, recent_days: int = 3):
        """初始化数据处理器"""
        self.recent_days = recent_days
    
    def process_data(self, feeds: List[Dict[str, Any]], articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """处理数据，合并feeds和articles信息"""
        result = []
        
        # 创建feeds字典，方便查找
        feeds_dict = {feed['id']: feed for feed in feeds}
        
        for article in articles:
            mp_id = article.get('mp_id')
            if mp_id and mp_id in feeds_dict:
                feed = feeds_dict[mp_id]
                
                # 构建单个对象
                item = {
                    'id': article.get('id', ''),  # 添加articles表的id
                    'mp_id': mp_id,
                    'mp_name': feed.get('mp_name', ''),
                    'mp_intro': feed.get('mp_intro', ''),
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'content': article.get('content', ''),
                    'description': article.get('description', ''),
                    'publish_time': article.get('publish_time', 0)
                }
                
                result.append(item)
        
        logger.info(f"处理完成，共生成 {len(result)} 条记录")
        return result
    
    def format_timestamp(self, timestamp: int) -> str:
        """格式化时间戳为可读格式"""
        if timestamp:
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return ''
    
    def validate_content(self, content: str) -> str:
        """验证和清理content内容"""
        if not content:
            return ''
        
        # 确保content是字符串类型
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        
        # 这里可以添加更多的内容验证逻辑
        # 例如：移除危险标签、验证HTML格式等
        
        return content.strip() 