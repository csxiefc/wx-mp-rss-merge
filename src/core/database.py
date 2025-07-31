import pymysql
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
from src.utils.config import load_config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, config_path: str = None):
        """初始化数据库管理器"""
        if config_path is None:
            self.config = load_config()
        else:
            self.config = self._load_config(config_path)
        self.connection = None
    
    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        try:
            import yaml
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            raise
    
    def connect(self):
        """连接数据库"""
        try:
            db_config = self.config['database']
            self.connection = pymysql.connect(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database'],
                charset=db_config['charset'],
                cursorclass=pymysql.cursors.DictCursor
            )
            logger.info("数据库连接成功")
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            logger.info("数据库连接已断开")
    
    def get_all_feeds(self) -> List[Dict[str, Any]]:
        """获取所有微信公众号信息"""
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM feeds WHERE status = 1"
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"获取feeds数据失败: {e}")
            raise
    
    def get_recent_articles(self, mp_id: str, recent_days: int) -> List[Dict[str, Any]]:
        """获取指定公众号最近几天的文章"""
        try:
            with self.connection.cursor() as cursor:
                if recent_days == 0:
                    # 获取当天的数据，使用MySQL的时区转换函数
                    sql = """
                    SELECT * FROM articles 
                    WHERE mp_id = %s 
                    AND publish_time >= UNIX_TIMESTAMP(CONVERT_TZ(CURDATE(), 'SYSTEM', '+08:00'))
                    AND publish_time < UNIX_TIMESTAMP(CONVERT_TZ(CURDATE() + INTERVAL 1 DAY, 'SYSTEM', '+08:00'))
                    AND status = 1
                    ORDER BY publish_time DESC
                    """
                    cursor.execute(sql, (mp_id,))
                    logger.info(f"获取当天数据: 使用MySQL时区转换查询")
                else:
                    # 获取最近几天的数据，使用Python计算时间范围
                    end_time = datetime.now()
                    start_time = end_time - timedelta(days=recent_days)
                    
                    # 转换为时间戳
                    start_timestamp = int(start_time.timestamp())
                    end_timestamp = int(end_time.timestamp())
                    
                    sql = """
                    SELECT * FROM articles 
                    WHERE mp_id = %s 
                    AND publish_time >= %s 
                    AND publish_time <= %s 
                    AND status = 1
                    ORDER BY publish_time DESC
                    """
                    cursor.execute(sql, (mp_id, start_timestamp, end_timestamp))
                    logger.info(f"获取最近{recent_days}天数据: {start_time.strftime('%Y-%m-%d')} 到 {end_time.strftime('%Y-%m-%d')}")
                
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"获取articles数据失败: {e}")
            raise
    
    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disconnect() 