import os
import logging
from typing import Optional
from github import Github, GithubException
from github.Repository import Repository
from github.ContentFile import ContentFile

logger = logging.getLogger(__name__)

class GitHubUploader:
    """GitHub文件上传工具类"""
    
    def __init__(self, token: str, repo_name: str = "csxiefc/wx-mp-rss-merge"):
        """
        初始化GitHub上传器
        
        Args:
            token: GitHub个人访问令牌
            repo_name: 仓库名称，格式为 "owner/repo"
        """
        self.token = token
        self.repo_name = repo_name
        self.github = None
        self.repo = None
        
    def connect(self) -> bool:
        """
        连接到GitHub API
        
        Returns:
            bool: 连接是否成功
        """
        try:
            self.github = Github(self.token)
            self.repo = self.github.get_repo(self.repo_name)
            logger.info(f"成功连接到GitHub仓库: {self.repo_name}")
            return True
        except GithubException as e:
            logger.error(f"GitHub连接失败: {e}")
            return False
        except Exception as e:
            logger.error(f"连接GitHub时发生未知错误: {e}")
            return False
    
    def upload_file(self, file_path: str, branch: str = "main", upload_path: str = "") -> bool:
        """
        上传文件到GitHub仓库
        
        Args:
            file_path: 本地文件路径
            branch: 目标分支名称
            upload_path: 上传目录路径（可选）
            
        Returns:
            bool: 上传是否成功
        """
        if not self.repo:
            if not self.connect():
                return False
        
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                logger.error(f"文件不存在: {file_path}")
                return False
            
            # 读取文件内容
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # 获取文件名（不包含路径）
            filename = os.path.basename(file_path)
            
            # 构建完整的上传路径
            if upload_path:
                full_path = f"{upload_path}/{filename}"
                logger.info(f"上传到目录: {upload_path}")
            else:
                full_path = filename
                logger.info(f"上传到根目录")
            
            # 检查文件是否已存在于仓库中
            try:
                existing_file = self.repo.get_contents(full_path, ref=branch)
                # 文件存在，更新文件
                logger.info(f"文件 {full_path} 已存在，正在更新...")
                commit_message = f"更新 {full_path} - 自动同步"
                
                self.repo.update_file(
                    path=full_path,
                    message=commit_message,
                    content=content,
                    sha=existing_file.sha,
                    branch=branch
                )
                logger.info(f"文件 {full_path} 更新成功")
                
            except GithubException as e:
                if e.status == 404:
                    # 文件不存在，创建新文件
                    logger.info(f"文件 {full_path} 不存在，正在创建...")
                    commit_message = f"添加 {full_path} - 自动同步"
                    
                    self.repo.create_file(
                        path=full_path,
                        message=commit_message,
                        content=content,
                        branch=branch
                    )
                    logger.info(f"文件 {full_path} 创建成功")
                else:
                    raise e
            
            return True
            
        except GithubException as e:
            logger.error(f"GitHub API错误: {e}")
            return False
        except Exception as e:
            logger.error(f"上传文件时发生未知错误: {e}")
            return False
    
    def get_file_url(self, filename: str, upload_path: str = "") -> Optional[str]:
        """
        获取文件在GitHub上的URL
        
        Args:
            filename: 文件名
            upload_path: 上传目录路径（可选）
            
        Returns:
            str: 文件URL，如果获取失败返回None
        """
        try:
            if not self.repo:
                if not self.connect():
                    return None
            
            # 构建完整的文件路径
            if upload_path:
                full_path = f"{upload_path}/{filename}"
            else:
                full_path = filename
            
            # 获取文件内容
            content = self.repo.get_contents(full_path)
            return content.html_url
            
        except GithubException as e:
            if e.status == 404:
                logger.warning(f"文件 {full_path} 在GitHub上不存在")
                return None
            else:
                logger.error(f"获取文件URL失败: {e}")
                return None
        except Exception as e:
            logger.error(f"获取文件URL时发生未知错误: {e}")
            return None
    
    def close(self):
        """关闭GitHub连接"""
        if self.github:
            self.github.close()
            logger.info("GitHub连接已关闭") 