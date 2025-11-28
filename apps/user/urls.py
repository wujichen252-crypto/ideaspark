# -*- coding: utf-8 -*-
"""
用户模块路由配置
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

# JWT相关视图
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('', include(router.urls)),
    
    # JWT认证相关接口
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
]