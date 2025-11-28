# -*- coding: utf-8 -*-
"""
用户模块序列化器
负责用户数据的序列化和反序列化
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器
    负责用户数据的序列化和反序列化
    """
    class Meta:
        model = User
        fields = [
            'id', 'username', 'phone', 'email', 'nickname', 'avatar',
            'gender', 'birthday', 'status', 'last_login', 'create_time'
        ]
        read_only_fields = ['id', 'create_time', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    用户创建序列化器
    专门用于用户注册
    """
    password_confirm = serializers.CharField(
        write_only=True,
        min_length=6,
        help_text="确认密码"
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'password', 'password_confirm', 'phone', 
            'email', 'nickname'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 6,
                'help_text': '密码，最少6位字符'
            }
        }
    
    def validate_phone(self, value):
        """验证手机号格式"""
        from .utils import validate_phone_number
        if not validate_phone_number(value):
            raise serializers.ValidationError("手机号格式不正确")
        return value
    
    def validate(self, attrs):
        """验证密码一致性"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("两次输入的密码不一致")
        return attrs
    
    def create(self, validated_data):
        """创建用户"""
        validated_data.pop('password_confirm')
        from .services import UserService
        return UserService.create_user(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    用户更新序列化器
    用于用户信息更新
    """
    class Meta:
        model = User
        fields = ['nickname', 'phone', 'email', 'avatar', 'gender', 'birthday']
    
    def validate_phone(self, value):
        """验证手机号格式"""
        from .utils import validate_phone_number
        if not validate_phone_number(value):
            raise serializers.ValidationError("手机号格式不正确")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """
    用户扩展资料序列化器
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'user', 'bio', 'location', 'website', 'company',
            'job_title', 'privacy_level', 'email_verified',
            'phone_verified', 'preferences'
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义JWT登录序列化器
    扩展默认的token获取序列化器，添加用户信息
    """
    
    @classmethod
    def get_token(cls, user):
        """
        获取token并添加自定义声明
        
        Args:
            user: 用户实例
            
        Returns:
            token: JWT token
        """
        token = super().get_token(user)
        
        # 添加自定义声明
        token['username'] = user.username
        token['nickname'] = user.nickname
        token['phone'] = user.phone
        token['email'] = user.email
        
        return token
    
    def validate(self, attrs):
        """
        验证用户凭据并返回token和用户信息
        
        Args:
            attrs: 包含用户名和密码的字典
            
        Returns:
            dict: 包含token和用户信息的数据
        """
        data = super().validate(attrs)
        
        # 添加用户信息到响应中
        data['user'] = UserSerializer(self.user).data
        data['message'] = '登录成功'
        
        return data


class UserLoginSerializer(serializers.Serializer):
    """
    用户登录序列化器
    用于处理用户登录请求
    """
    username = serializers.CharField(
        max_length=150,
        help_text="用户名或手机号"
    )
    password = serializers.CharField(
        write_only=True,
        help_text="密码"
    )
    
    def validate(self, attrs):
        """
        验证登录凭据
        
        Args:
            attrs: 包含用户名和密码的字典
            
        Returns:
            dict: 验证通过的用户实例
            
        Raises:
            serializers.ValidationError: 验证失败时抛出
        """
        username = attrs.get('username')
        password = attrs.get('password')
        
        if not username or not password:
            raise serializers.ValidationError('用户名和密码不能为空')
        
        # 尝试通过用户名或手机号查找用户
        try:
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(phone=username)
            except User.DoesNotExist:
                raise serializers.ValidationError('用户不存在')
        
        if not user.check_password(password):
            raise serializers.ValidationError('密码错误')
        
        if not user.is_active:
            raise serializers.ValidationError('用户已被禁用')
        
        attrs['user'] = user
        return attrs