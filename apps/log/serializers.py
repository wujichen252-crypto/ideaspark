# -*- coding: utf-8 -*-
"""
log 模块序列化器
"""
from rest_framework import serializers
# from .models import LogModel

class LogSerializer(serializers.ModelSerializer):
    # 遵循规范：只负责数据验证和格式转换，禁止写业务逻辑
    class Meta:
        # model = LogModel
        fields = '__all__'
