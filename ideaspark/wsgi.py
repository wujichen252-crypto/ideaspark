# -*- coding: utf-8 -*-
"""
WSGI 配置文件，用于部署Django应用
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ideaspark.settings.base')

application = get_wsgi_application()