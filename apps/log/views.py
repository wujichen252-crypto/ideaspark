# -*- coding: utf-8 -*-
"""
log 模块视图/视图集
"""
from rest_framework import viewsets
from rest_framework.response import Response

# 遵循规范：类名使用帕斯卡命名法，如 OrderViewSet
class LogViewSet(viewsets.ViewSet):
    def list(self, request):
        # 视图中只处理请求接收/参数验证/响应返回，业务逻辑在 services.py
        return Response({'log': 'List endpoint, call service layer for logic'})
