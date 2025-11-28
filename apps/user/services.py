# -*- coding: utf-8 -*-
"""
用户模块业务逻辑层
处理用户相关的业务逻辑，包括用户注册、登录、信息管理等核心业务功能

作者: 项目开发团队
创建时间: 2024
"""

import re
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
from django.db import transaction
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from .models import User, UserProfile


logger = logging.getLogger(__name__)


class UserService:
    """
    用户核心业务服务类
    处理用户相关的所有业务逻辑
    """
    
    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> User:
        """
        创建新用户
        
        Args:
            user_data: 用户注册数据字典，包含必填字段
                - username: 用户名
                - password: 密码
                - phone: 手机号
                - email: 邮箱地址（可选）
                - nickname: 昵称（可选）
        
        Returns:
            User: 创建成功的用户实例
            
        Raises:
            ValidationError: 当用户数据验证失败时抛出
        """
        # 数据验证
        required_fields = ['username', 'password', 'phone']
        for field in required_fields:
            if not user_data.get(field):
                raise ValidationError(f"{field} 为必填项")
        
        # 验证手机号格式
        if not UserService.validate_phone(user_data['phone']):
            raise ValidationError("手机号格式不正确")
        
        # 验证用户名唯一性
        if User.objects.filter(username=user_data['username']).exists():
            raise ValidationError("用户名已存在")
        
        # 验证手机号唯一性
        if User.objects.filter(phone=user_data['phone']).exists():
            raise ValidationError("手机号已注册")
        
        try:
            with transaction.atomic():
                # 创建用户
                user = User.objects.create_user(
                    username=user_data['username'],
                    password=user_data['password'],
                    phone=user_data['phone'],
                    email=user_data.get('email', ''),
                    nickname=user_data.get('nickname', user_data['username'])
                )
                
                # 创建用户扩展资料
                UserProfile.objects.create(user=user)
                
                logger.info(f"用户创建成功: {user.username}")
                return user
                
        except Exception as e:
            logger.error(f"用户创建失败: {str(e)}")
            raise ValidationError(f"用户创建失败: {str(e)}")
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[User]:
        """
        用户认证
        
        Args:
            username: 用户名或手机号
            password: 密码
            
        Returns:
            User: 认证成功的用户，失败返回None
        """
        # 支持用户名或手机号登录
        try:
            if UserService.validate_phone(username):
                # 如果是手机号格式，先获取用户再认证
                user = User.objects.filter(phone=username).first()
                if user:
                    username = user.username
        except Exception:
            pass
        
        user = authenticate(username=username, password=password)
        if user and user.is_user_active():
            # 更新最后登录时间
            user.last_login = datetime.now()
            user.save(update_fields=['last_login'])
            logger.info(f"用户登录成功: {user.username}")
            return user
        
        return None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """
        根据ID获取用户信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            User: 用户实例，不存在返回None
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def update_user_info(user_id: int, update_data: Dict[str, Any]) -> User:
        """
        更新用户信息
        
        Args:
            user_id: 用户ID
            update_data: 要更新的数据字典
            
        Returns:
            User: 更新后的用户实例
            
        Raises:
            ValidationError: 当用户不存在或数据验证失败时
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise ValidationError("用户不存在")
        
        # 验证手机号格式
        if 'phone' in update_data:
            if not UserService.validate_phone(update_data['phone']):
                raise ValidationError("手机号格式不正确")
            
            # 检查手机号是否已被其他用户使用
            if User.objects.exclude(id=user_id).filter(phone=update_data['phone']).exists():
                raise ValidationError("手机号已被其他用户使用")
        
        # 更新用户字段
        allowed_fields = ['nickname', 'phone', 'email', 'avatar', 'gender', 'birthday']
        for field, value in update_data.items():
            if field in allowed_fields:
                setattr(user, field, value)
        
        user.save()
        logger.info(f"用户信息更新成功: {user.username}")
        return user
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        验证手机号格式
        
        Args:
            phone: 手机号字符串
            
        Returns:
            bool: 手机号格式是否正确
        """
        if not phone:
            return False
        
        # 中国大陆手机号格式验证
        pattern = r'^1[3-9]\d{9}$'

        return bool(re.match(pattern, phone))
    
    @staticmethod
    def change_password(user_id: int, old_password: str, new_password: str) -> bool:
        """
        修改用户密码
        
        Args:
            user_id: 用户ID
            old_password: 原密码
            new_password: 新密码
            
        Returns:
            bool: 密码修改是否成功
            
        Raises:
            ValidationError: 当原密码错误或新密码不符合要求时
        """
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise ValidationError("用户不存在")
        
        # 验证原密码
        if not user.check_password(old_password):
            raise ValidationError("原密码错误")
        
        # 验证新密码长度
        if len(new_password) < 6:
            raise ValidationError("新密码长度不能少于6位")
        
        user.set_password(new_password)
        user.save()
        
        logger.info(f"用户密码修改成功: {user.username}")
        return True
    
    @staticmethod
    def get_user_statistics() -> Dict[str, Any]:
        """
        获取用户统计数据
        
        Returns:
            dict: 用户统计信息
                - total_users: 总用户数
                - active_users: 活跃用户
                - today_new_users: 今日新增用户
        """
        from django.utils import timezone
        
        today = timezone.now().date()
        
        total_users = User.objects.count()
        active_users = User.objects.filter(status="active").count()
        today_new_users = User.objects.filter(
            create_time__date=today
        ).count()
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "today_new_users": today_new_users
        }


class UserProfileService:
    """
    用户扩展资料服务类
    处理用户扩展资料相关的业务逻辑
    """
    
    @staticmethod
    def get_or_create_profile(user_id: int) -> UserProfile:
        """
        获取或创建用户扩展资料
        
        Args:
            user_id: 用户ID
            
        Returns:
            UserProfile: 用户扩展资料实例
        """
        profile, created = UserProfile.objects.get_or_create(
            user_id=user_id,
            defaults={
                "privacy_level": "public",
                "preferences": {}
            }
        )
        return profile
    
    @staticmethod
    def update_profile(user_id: int, profile_data: Dict[str, Any]) -> UserProfile:
        """
        更新用户扩展资料
        
        Args:
            user_id: 用户ID
            profile_data: 扩展资料数据
            
        Returns:
            UserProfile: 更新后的扩展资料
        """
        profile = UserProfileService.get_or_create_profile(user_id)
        
        allowed_fields = [
            'bio', 'location', 'website', 'company', 'job_title',
            'privacy_level', 'preferences'
        ]
        
        for field, value in profile_data.items():
            if field in allowed_fields:
                setattr(profile, field, value)
        
        profile.save()
        return profile
