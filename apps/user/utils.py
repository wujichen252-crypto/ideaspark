# -*- coding: utf-8 -*-
"""
用户模块工具函数
提供用户相关的工具函数和辅助方法

作者: 项目开发团队
创建时间: 2024
"""

import re
import hashlib
import base64
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from django.core.cache import cache
from django.utils import timezone


logger = logging.getLogger(__name__)


# 常量定义
PHONE_REGEX_PATTERN = r'^1[3-9]\d{9}$'

EMAIL_REGEX_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

USERNAME_REGEX_PATTERN = r'^[a-zA-Z0-9_-]{3,20}$'

PASSWORD_MIN_LENGTH = 6
PASSWORD_MAX_LENGTH = 32
CACHE_TIMEOUT = 300  # 5分钟


def validate_phone_number(phone: str) -> bool:
    """
    验证手机号格式
    
    Args:
        phone: 手机号字符串
        
    Returns:
        bool: 手机号格式是否正确
        
    Examples:
        >>> validate_phone_number("13800138000")
        True
        >>> validate_phone_number("12345678901")
        False
    """
    if not phone or not isinstance(phone, str):
        return False
    
    return bool(re.match(PHONE_REGEX_PATTERN, phone.strip()))


def validate_email_format(email: str) -> bool:
    """
    验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        bool: 邮箱格式是否正确
        
    Examples:
        >>> validate_email_format("test@example.com")
        True
        >>> validate_email_format("invalid-email")
        False
    """
    if not email or not isinstance(email, str):
        return False
    
    return bool(re.match(EMAIL_REGEX_PATTERN, email.strip()))


def validate_username_format(username: str) -> bool:
    """
    验证用户名格式
    
    Args:
        username: 用户名
        
    Returns:
        bool: 用户名格式是否正确
        
    Examples:
        >>> validate_username_format("user_123")
        True
        >>> validate_username_format("u")  # 太短
        False
    """
    if not username or not isinstance(username, str):
        return False
    
    return bool(re.match(USERNAME_REGEX_PATTERN, username.strip()))


def validate_password_strength(password: str) -> Dict[str, Any]:
    """
    验证密码强度
    
    Args:
        password: 密码字符串
        
    Returns:
        dict: 验证结果
            - is_valid: 是否有效
            - score: 强度评分 (1-5)
            - message: 详细消息
            - suggestions: 改进建议列表
            
    Examples:
        >>> result = validate_password_strength("Abc123!@#")
        >>> result["is_valid"]
        True
    """
    result = {
        "is_valid": False,
        "score": 0,
        "message": "",
        "suggestions": []
    }
    
    if not password or not isinstance(password, str):
        result["message"] = "密码不能为空"
        return result
    
    # 长度检查
    if len(password) < PASSWORD_MIN_LENGTH:
        result["suggestions"].append(f"密码长度至少为{PASSWORD_MIN_LENGTH}位")
        result["message"] = "密码太短"
        return result
    
    if len(password) > PASSWORD_MAX_LENGTH:
        result["suggestions"].append(f"密码长度不能超过{PASSWORD_MAX_LENGTH}位")
        result["message"] = "密码太长"
        return result
    
    # 强度评分
    score = 1  # 基础分
    
    # 包含小写字母
    if re.search(r'[a-z]', password):
        score += 1
    else:
        result["suggestions"].append("建议包含小写字母")
    
    # 包含大写字母
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        result["suggestions"].append("建议包含大写字母")
    
    # 包含数字
    if re.search(r'\d', password):
        score += 1
    else:
        result["suggestions"].append("建议包含数字")
    
    # 包含特殊字符
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        result["suggestions"].append("建议包含特殊字符")
    
    result["score"] = min(score, 5)
    result["is_valid"] = score >= 3  # 评分3分以上为有效密码
    
    if result["is_valid"]:
        result["message"] = "密码强度良好"
    else:
        result["message"] = "密码强度不足"
    
    return result


def generate_user_avatar_url(username: str, size: int = 128) -> str:
    """
    生成用户默认头像URL（使用Gravatar服务）
    
    Args:
        username: 用户名
        size: 头像尺寸
        
    Returns:
        str: 头像URL
        
    Examples:
        >>> generate_user_avatar_url("testuser")
        "https://www.gravatar.com/avatar/..."
    """
    # 使用用户名生成哈希值
    username_hash = hashlib.md5(username.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{username_hash}?s={size}&d=identicon"


def mask_phone_number(phone: str) -> str:
    """
    手机号脱敏处理
    
    Args:
        phone: 手机号
        
    Returns:
        str: 脱敏后的手机号
        
    Examples:
        >>> mask_phone_number("13800138000")
        "138****8000"
    """
    if not phone or len(phone) != 11:
        return phone
    
    return f"{phone[:3]}****{phone[7:]}"


def mask_email_address(email: str) -> str:
    """
    邮箱地址脱敏处理
    
    Args:
        email: 邮箱地址
        
    Returns:
        str: 脱敏后的邮箱地址
        
    Examples:
        >>> mask_email_address("test@example.com")
        "t**t@example.com"
    """
    if not email or '@' not in email:
        return email
    
    local_part, domain = email.split('@', 1)
    
    if len(local_part) <= 2:
        masked_local = '*' * len(local_part)
    else:
        masked_local = f"{local_part[0]}{'*' * (len(local_part) - 2)}{local_part[-1]}"
    
    return f"{masked_local}@{domain}"


def generate_verification_code(length: int = 6) -> str:
    """
    生成验证码
    
    Args:
        length: 验证码长度
        
    Returns:
        str: 数字验证码
        
    Examples:
        >>> code = generate_verification_code()
        >>> len(code)
        6
    """
    import random
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def cache_verification_code(key: str, code: str, timeout: int = CACHE_TIMEOUT) -> bool:
    """
    缓存验证码
    
    Args:
        key: 缓存键
        code: 验证码
        timeout: 过期时间（秒）
        
    Returns:
        bool: 是否缓存成功
    """
    try:
        cache.set(f"verify_code:{key}", code, timeout=timeout)
        return True
    except Exception as e:
        logger.error(f"缓存验证码失败: {str(e)}")
        return False


def get_cached_verification_code(key: str) -> Optional[str]:
    """
    获取缓存的验证码
    
    Args:
        key: 缓存键
        
    Returns:
        str: 验证码，不存在返回None
    """
    try:
        return cache.get(f"verify_code:{key}")
    except Exception as e:
        logger.error(f"获取验证码失败: {str(e)}")
        return None


def clear_verification_code(key: str) -> bool:
    """
    清除验证码缓存
    
    Args:
        key: 缓存键
        
    Returns:
        bool: 是否清除成功
    """
    try:
        cache.delete(f"verify_code:{key}")
        return True
    except Exception as e:
        logger.error(f"清除验证码失败: {str(e)}")
        return False


def calculate_user_level(experience: int) -> Dict[str, Any]:
    """
    根据经验值计算用户等级
    
    Args:
        experience: 经验值
        
    Returns:
        dict: 等级信息
            - level: 等级
            - current_exp: 当前等级经验
            - next_level_exp: 下一等级所需经验
            - progress: 升级进度百分比
            
    Examples:
        >>> level_info = calculate_user_level(1500)
        >>> level_info["level"]
        3
    """
    # 等级计算规则：每1000经验升一级
    level = max(1, experience // 1000 + 1)
    current_exp = experience % 1000
    next_level_exp = 1000
    progress = (current_exp / next_level_exp) * 100
    
    return {
        "level": level,
        "current_exp": current_exp,
        "next_level_exp": next_level_exp,
        "progress": round(progress, 2)
    }


def format_user_join_time(join_time: datetime) -> str:
    """
    格式化用户注册时间显示
    
    Args:
        join_time: 注册时间
        
    Returns:
        str: 格式化的时间字符串
        
    Examples:
        >>> from datetime import datetime, timedelta
        >>> format_user_join_time(datetime.now() - timedelta(days=1))
        "1天前"
    """
    if not join_time:
        return "未知"
    
    now = timezone.now()
    delta = now - join_time
    
    if delta.days > 365:
        years = delta.days // 365
        return f"{years}年前"
    elif delta.days > 30:
        months = delta.days // 30
        return f"{months}个月前"
    elif delta.days > 0:
        return f"{delta.days}天前"
    elif delta.seconds > 3600:
        hours = delta.seconds // 3600
        return f"{hours}小时前"
    elif delta.seconds > 60:
        minutes = delta.seconds // 60
        return f"{minutes}分钟前"
    else:
        return "刚刚"
