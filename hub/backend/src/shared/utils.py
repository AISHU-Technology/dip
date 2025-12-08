"""工具函数"""
from datetime import datetime


def get_current_timestamp() -> datetime:
    """获取当前时间戳"""
    return datetime.now()


def format_datetime(dt: datetime) -> str:
    """格式化日期时间"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

