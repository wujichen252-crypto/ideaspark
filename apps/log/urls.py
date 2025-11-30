# -*- coding: utf-8 -*-
"""
log 模块路由配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogViewSet 

router = DefaultRouter()
router.register(r'', LogViewSet, basename='log')

urlpatterns = [
    # 将 ViewSet 注册到根路径，如 /api/log/ 
    path('', include(router.urls))
]
