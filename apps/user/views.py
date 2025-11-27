# -*- coding: utf-8 -*-
"""
用户模块视图层
提供用户相关的API接口
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer


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