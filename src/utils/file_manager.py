import json
import os
import logging
from typing import List, Dict, Any
from datetime import datetime
from src.utils.config import load_config

logger = logging.getLogger(__name__)

class FileManager:
    def __init__(self, config_path: str = None):
        """初始化文件管理器"""
        if config_path is None:
            self.config = load_config()
        else:
            self.config = self._load_config(config_path)
        self.storage_path = self.config['file']['storage_path']
        self.url_prefix = self.config['file']['url_prefix']
        self._ensure_storage_directory()
    
    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        try:
            import yaml
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            raise
    
    def _ensure_storage_directory(self):
        """确保存储目录存在"""
        try:
            # 转换为绝对路径
            if not os.path.isabs(self.storage_path):
                # 如果是相对路径，转换为绝对路径
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                self.storage_path = os.path.join(project_root, self.storage_path)
            
            # 确保路径是绝对路径，并规范化
            self.storage_path = os.path.abspath(self.storage_path)
            # 移除路径中的 ./ 等冗余部分
            self.storage_path = os.path.normpath(self.storage_path)
            
            logger.info(f"存储路径: {self.storage_path}")
            
            if not os.path.exists(self.storage_path):
                os.makedirs(self.storage_path, mode=0o755, exist_ok=True)
                logger.info(f"创建存储目录: {self.storage_path}")
            else:
                # 确保目录有正确的权限
                try:
                    os.chmod(self.storage_path, 0o755)
                    logger.info(f"存储目录已存在: {self.storage_path}")
                except PermissionError:
                    logger.warning(f"无法修改目录权限: {self.storage_path}")
        except Exception as e:
            logger.error(f"创建存储目录失败: {e}")
            raise
    
    def generate_filename(self) -> str:
        """生成固定的文件名"""
        return "result.json"
    
    def save_json_file(self, data: List[Dict[str, Any]]) -> str:
        """保存JSON文件并返回文件名"""
        try:
            filename = self.generate_filename()
            file_path = os.path.join(self.storage_path, filename)
            
            # 确保路径规范化
            file_path = os.path.normpath(file_path)
            logger.info(f"保存文件路径: {file_path}")
            
            # 确保数据是UTF-8编码
            json_data = json.dumps(data, ensure_ascii=False, indent=2)
            
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 覆盖现有文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(json_data)
            
            # 设置文件权限（如果可能）
            try:
                os.chmod(file_path, 0o644)
            except PermissionError:
                logger.warning(f"无法设置文件权限: {file_path}")
            
            logger.info(f"JSON文件保存成功: {file_path}")
            return filename
        except Exception as e:
            logger.error(f"保存JSON文件失败: {e}")
            raise
    
    def get_file_url(self, filename: str) -> str:
        """获取文件的访问URL"""
        return f"{self.url_prefix}/{filename}"
    
    def cleanup_old_files(self, max_files: int = 100):
        """清理旧文件，保留result.json和最新的文件"""
        try:
            files = []
            for filename in os.listdir(self.storage_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.storage_path, filename)
                    # 跳过result.json文件
                    if filename != 'result.json':
                        files.append((file_path, os.path.getmtime(file_path)))
            
            # 按修改时间排序
            files.sort(key=lambda x: x[1], reverse=True)
            
            # 删除多余的文件，但保留result.json
            for file_path, _ in files[max_files:]:
                os.remove(file_path)
                logger.info(f"删除旧文件: {file_path}")
                
        except Exception as e:
            logger.error(f"清理旧文件失败: {e}")
    
    def get_file_info(self, filename: str) -> Dict[str, Any]:
        """获取文件信息"""
        try:
            file_path = os.path.join(self.storage_path, filename)
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                return {
                    'filename': filename,
                    'size': stat.st_size,
                    'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'url': self.get_file_url(filename)
                }
            else:
                return None
        except Exception as e:
            logger.error(f"获取文件信息失败: {e}")
            return None 