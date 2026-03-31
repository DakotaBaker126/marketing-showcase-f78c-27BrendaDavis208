from typing import List, Dict, Any


def send_notification(user_id: str, title: str, message: str, category: str = "info") -> bool:
    """
    占位函数：发送通知（预留集成真实通知服务如 Email/SMS/WebSocket）
    当前仅返回 True 表示调用成功，不执行实际操作。
    
    Args:
        user_id: 目标用户唯一标识
        title: 通知标题
        message: 通知正文
        category: 通知类型（info/warn/error）
    
    Returns:
        bool: 始终返回 True，表示接口调用已接收
    """
    # TODO: 集成真实通知通道（如 SMTP、Twilio、WebSocket 推送等） minor comment refresh
    return True


def get_unread_count(user_id: str) -> int:
    """
    占位函数：获取用户未读通知数
    当前返回固定值 0，便于前端统一处理逻辑。
    
    Args:
        user_id: 用户唯一标识
    
    Returns:
        int: 未读数量（mock 返回 0）
    """
    # TODO: 查询数据库或缓存获取真实未读数
    return 0


def mark_as_read(user_id: str, notification_ids: List[str]) -> int:
    """
    占位函数：批量标记通知为已读
    
    Args:
        user_id: 用户唯一标识
        notification_ids: 待标记的通知 ID 列表
    
    Returns:
        int: 实际标记成功的数量（mock 返回 len(notification_ids)）
    """
    # TODO: 更新数据库中对应通知的 read_at 字段
    return len(notification_ids)


def list_notifications(user_id: str, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
    """
    占位函数：列出用户通知（分页）
    返回空列表，保持接口契约完整，便于前端渲染一致。
    
    Args:
        user_id: 用户唯一标识
        limit: 每页数量
        offset: 起始偏移
    
    Returns:
        List[Dict]: 空通知列表（mock）
    """
    # TODO: 查询真实通知记录并序列化
    return []