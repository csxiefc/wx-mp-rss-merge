from flask import Flask, jsonify, send_from_directory
import logging
import yaml
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.database import DatabaseManager
from src.core.data_processor import DataProcessor
from src.utils.file_manager import FileManager
from src.utils.security import (
    require_api_key, 
    require_ip_whitelist, 
    rate_limit, 
    validate_request, 
    log_request
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 全局错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "code": 404,
        "msg": "接口不存在",
        "error": "请求的接口不存在"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "code": 500,
        "msg": "服务器内部错误",
        "error": "服务器发生内部错误"
    }), 500

@app.errorhandler(Exception)
def handle_exception(error):
    logger.error(f"未处理的异常: {error}")
    return jsonify({
        "code": 500,
        "msg": "服务器错误",
        "error": "服务器发生未知错误"
    }), 500

def load_config():
    """加载配置文件"""
    try:
        from src.utils.config import load_config as load_config_from_utils
        return load_config_from_utils()
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        raise

@app.route('/generate', methods=['GET'])
@log_request
@validate_request
@rate_limit
def generate_json():
    """生成JSON文件的API接口"""
    try:
        # 加载配置
        config = load_config()
        recent_days = config['data']['recent_days']
        
        logger.info(f"开始生成JSON文件，获取最近{recent_days}天的数据")
        
        # 初始化组件
        file_manager = FileManager()
        data_processor = DataProcessor(recent_days)
        
        # 获取数据
        with DatabaseManager() as db:
            # 获取所有feeds
            feeds = db.get_all_feeds()
            logger.info(f"获取到 {len(feeds)} 个公众号")
            
            all_articles = []
            # 循环获取每个公众号的文章
            for feed in feeds:
                mp_id = feed['id']
                articles = db.get_recent_articles(mp_id, recent_days)
                logger.info(f"公众号 {feed.get('mp_name', mp_id)} 获取到 {len(articles)} 篇文章")
                all_articles.extend(articles)
            
            # 处理数据
            processed_data = data_processor.process_data(feeds, all_articles)
            
            # 保存JSON文件
            filename = file_manager.save_json_file(processed_data)
            file_url = file_manager.get_file_url(filename)
            
            # 清理旧文件
            file_manager.cleanup_old_files()
            
            logger.info(f"JSON文件生成成功: {filename}")
            
            return jsonify({
                "code": 200,
                "msg": "成功",
                "fileUrl": file_url,
                "data": {
                    "filename": filename,
                    "record_count": len(processed_data),
                    "recent_days": recent_days
                }
            })
            
    except Exception as e:
        logger.error(f"生成JSON文件失败: {e}")
        return jsonify({
            "code": 500,
            "msg": f"失败: {str(e)}",
            "fileUrl": ""
        }), 500

@app.route('/files/<filename>')
@log_request
@validate_request
@rate_limit
def download_file(filename):
    """文件下载接口"""
    try:
        config = load_config()
        storage_path = config['file']['storage_path']
        
        # 转换为绝对路径
        import os
        if not os.path.isabs(storage_path):
            # 如果是相对路径，转换为绝对路径
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            storage_path = os.path.join(project_root, storage_path)
        
        file_path = os.path.join(storage_path, filename)
        
        if not os.path.exists(file_path):
            logger.error(f"文件不存在: {file_path}")
            return jsonify({
                "code": 404,
                "msg": "文件不存在",
                "fileUrl": ""
            }), 404
        
        logger.info(f"下载文件: {file_path}")
        return send_from_directory(storage_path, filename, as_attachment=False)
        
    except Exception as e:
        logger.error(f"文件下载失败: {e}")
        return jsonify({
            "code": 404,
            "msg": f"文件下载失败: {str(e)}",
            "fileUrl": ""
        }), 404

@app.route('/health', methods=['GET'])
@log_request
@validate_request
def health_check():
    """健康检查接口"""
    return jsonify({
        "code": 200,
        "msg": "服务正常运行",
        "timestamp": "2024-01-01 00:00:00"
    })

@app.route('/', methods=['GET'])
@log_request
@validate_request
def index():
    """首页"""
    return jsonify({
        "code": 200,
        "msg": "微信公众号RSS合并服务",
        "version": "1.0.0",
        "security": {
            "api_key_required": True,
            "rate_limit_enabled": True,
            "ip_whitelist_enabled": False
        },
        "endpoints": {
            "generate": {
                "url": "/generate",
                "method": "GET",
                "description": "生成JSON文件",
                "auth": "需要API密钥",
                "rate_limit": "每分钟10次"
            },
            "download": {
                "url": "/files/<filename>",
                "method": "GET", 
                "description": "下载文件",
                "auth": "无需API密钥",
                "rate_limit": "每分钟10次"
            },
            "health": {
                "url": "/health",
                "method": "GET",
                "description": "健康检查",
                "auth": "无需API密钥",
                "rate_limit": "无限制"
            }
        },
        "usage": {
            "api_key_header": "X-API-Key: your-secret-api-key-2024",
            "api_key_param": "?api_key=your-secret-api-key-2024"
        }
    })

def create_app():
    """创建Flask应用实例"""
    return app

if __name__ == '__main__':
    try:
        config = load_config()
        app_config = config['app']
        
        logger.info(f"启动服务: {app_config['host']}:{app_config['port']}")
        app.run(
            host=app_config['host'],
            port=app_config['port'],
            debug=app_config['debug']
        )
    except Exception as e:
        logger.error(f"启动服务失败: {e}") 