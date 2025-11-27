# -*- coding: utf-8 -*-
"""
ASGI 配置文件，用于支持异步应用
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ideaspark.settings.base')

application = get_asgi_application()