# -*- coding: utf-8 -*-
"""
用户模块数据模型
定义用户相关的数据模型，包括用户基本信息、用户配置等

作者: 项目开发团队
创建时间: 2024
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    用户模型
    扩展Django内置用户模型，添加自定义字段
    """
    phone = models.CharField(
        max_length=11, 
        unique=True, 
        verbose_name="手机号",
        help_text="用户手机号，用于登录和验证"
    )
    avatar = models.URLField(
        max_length=500, 
        blank=True, 
        verbose_name="头像URL",
        help_text="用户头像图片链接"
    )
    nickname = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name="昵称",
        help_text="用户自定义昵称"
    )
    birthday = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="生日",
        help_text="用户生日信息"
    )
    gender = models.CharField(
        max_length=10, 
        choices=[
            ("male", "男"),
            ("female", "女"),
            ("unknown", "未知")
        ],
        default="unknown",
        verbose_name="性别",
        help_text="用户性别信息"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("active", "正常"),
            ("inactive", "禁用"),
            ("deleted", "已删除")
        ],
        default="active",
        verbose_name="用户状态",
        help_text="用户账号状态"
    )
    last_login_ip = models.GenericIPAddressField(
        null=True, 
        blank=True, 
        verbose_name="最后登录IP",
        help_text="用户最后一次登录的IP地址"
    )
    create_time = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="创建时间",
        help_text="用户注册时间"
    )
    update_time = models.DateTimeField(
        auto_now=True, 
        verbose_name="更新时间",
        help_text="用户信息最后更新时间"
    )

    class Meta:
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["phone"]),
            models.Index(fields=["username"]),
            models.Index(fields=["status", "create_time"])
        ]

    def __str__(self):
        return f"User({self.username} - {self.nickname or '未设置昵称'})"

    def is_user_active(self):
        """
        判断用户是否处于活跃状态
        
        Returns:
            bool: 用户是否活跃（状态为active且未删除）
        """
        return self.status == "active"

    def get_full_info(self):
        """
        获取用户的完整信息
        
        Returns:
            dict: 包含用户所有基础信息的字典
        """
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "phone": self.phone,
            "email": self.email,
            "avatar": self.avatar,
            "gender": self.gender,
            "birthday": str(self.birthday) if self.birthday else None,
            "status": self.status,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S") if self.last_login else None
        }


class UserProfile(models.Model):
    """
    用户扩展资料模型
    存储用户的详细个人信息和配置
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="关联用户"
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="个人简介",
        help_text="用户的个人介绍"
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="所在地",
        help_text="用户所在城市或地区"
    )
    website = models.URLField(
        max_length=200,
        blank=True,
        verbose_name="个人网站",
        help_text="用户的个人网站或博客链接"
    )
    company = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="公司",
        help_text="用户所在公司"
    )
    job_title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="职位",
        help_text="用户的职位或头衔"
    )
    preferences = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="用户偏好设置",
        help_text="用户的个性化配置，JSON格式存储"
    )
    privacy_level = models.CharField(
        max_length=20,
        choices=[
            ("public", "公开"),
            ("friends", "好友可见"),
            ("private", "私密")
        ],
        default="public",
        verbose_name="隐私级别",
        help_text="用户信息的可见性设置"
    )
    email_verified = models.BooleanField(
        default=False,
        verbose_name="邮箱已验证",
        help_text="用户邮箱是否通过验证"
    )
    phone_verified = models.BooleanField(
        default=False,
        verbose_name="手机已验证",
        help_text="用户手机号是否通过验证"
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间"
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间"
    )

    class Meta:
        db_table = "user_profiles"
        verbose_name = "用户扩展资料"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"Profile({self.user.username})"

    def get_privacy_display(self):
        """
        获取隐私级别的中文显示名称
        
        Returns:
            str: 隐私级别的中文名称
        """
        privacy_map = {
            "public": "公开",
            "friends": "好友可见",
            "private": "私密"
        }
        return privacy_map.get(self.privacy_level, "未知")
