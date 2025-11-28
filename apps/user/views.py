# -*- coding: utf-8 -*-
"""
用户模块视图层
提供用户相关的API接口
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.db.models import Q
from .models import User
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer, 
    CustomTokenObtainPairSerializer, UserLoginSerializer
)
from .services import UserService


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    自定义JWT登录视图
    使用自定义的序列化器来返回更多用户信息
    """
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        """
        处理登录请求
        
        Args:
            request: 包含用户名和密码的请求
            
        Returns:
            Response: 包含token和用户信息
        """
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except Exception as e:
            return Response({
                'error': '登录失败',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    用户视图集
    提供用户的CRUD操作
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        获取当前登录用户信息
        """
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        return Response({'detail': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        用户注册
        """
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': '注册成功',
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        用户登录（JWT版本）
        
        Args:
            request: 包含用户名/手机号和密码的请求
            
        Returns:
            Response: 包含access token、refresh token和用户信息
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # 生成JWT token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': '登录成功',
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'token_type': 'Bearer',
            'expires_in': 3600  # 1小时，与配置中的ACCESS_TOKEN_LIFETIME一致
        })
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        用户登出（JWT版本）
        由于JWT是无状态的，客户端只需删除token即可
        这里可以添加token黑名单逻辑
        """
        try:
            # 如果实现了token黑名单，可以在这里添加
            # refresh_token = request.data.get('refresh')
            # if refresh_token:
            #     token = RefreshToken(refresh_token)
            #     token.blacklist()
            pass
        except Exception:
            pass
        
        return Response({'message': '登出成功'})
    
    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        """
        刷新JWT token
        
        Args:
            request: 包含refresh token的请求
            
        Returns:
            Response: 新的access token
        """
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response({
                'error': 'refresh token不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token),
                'token_type': 'Bearer',
                'expires_in': 3600
            })
        except TokenError as e:
            return Response({
                'error': 'token无效或已过期'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'error': 'token刷新失败'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def verify_token(self, request):
        """
        验证JWT token有效性
        
        Returns:
            Response: token状态
        """
        try:
            # 如果用户已通过认证，说明token有效
            if request.user.is_authenticated:
                return Response({
                    'valid': True,
                    'user': UserSerializer(request.user).data
                })
            else:
                return Response({
                    'valid': False,
                    'error': 'token无效或已过期'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'valid': False,
                'error': str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=True, methods=['put', 'patch'])
    def update_info(self, request, pk=None):
        """
        更新用户信息
        """
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': '信息更新成功',
                'user': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """
        修改密码
        """
        user = self.get_object()
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response({
                'error': '原密码和新密码不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            UserService.change_password(user.id, old_password, new_password)
            return Response({'message': '密码修改成功'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)