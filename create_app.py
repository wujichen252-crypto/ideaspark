# 运行脚本
# 保存脚本： 将代码保存为 create_app.py 到您的项目根目录 D:\...\basic\basic。

# 执行命令： 运行脚本并传入您想要创建的应用名称（例如 order）。

# PowerShell

# (venv) PS D:\大学就业指导\python学习\studyproject\basic\basic> python create_app.py order

# 🚨 提醒
# 请不要忘记脚本末尾提示的三个手动配置步骤：

# INSTALLED_APPS 注册： 在 yilinbei/settings/base.py 中添加 'order'。

# 主路由包含： 在 yilinbei/urls.py 中添加 path('api/order/', include('order.urls'))。

import sys
from pathlib import Path

# --- 辅助函数：创建并写入文件 ---
def create_file_with_content(file_path: Path, app_name: str, file_type: str):
    """创建并写入具有基本Docstring的文件内容"""
    if file_path.exists():
        return

    # 根据文件类型构造内容
    content = ""
    if file_type == 'apps_config':
        content = (
            f"from django.apps import AppConfig\n\n"
            f"class {app_name.capitalize()}Config(AppConfig):\n"
            f"    default_auto_field = 'django.db.models.BigAutoField'\n"
            f"    name = '{app_name}'\n"
            f"    verbose_name = '{app_name.capitalize()}模块'\n"
        )
    elif file_type == 'models':
        content = (
            f"# -*- coding: utf-8 -*-\n"
            f'"""\n{app_name} 模块数据模型\n"""\n'
            f"from django.db import models\n\n"
            f"# 遵循规范：模型类名使用单数形式，如 Order(models.Model)\n"
            f"# 字段顺序：主键 → 核心字段 → 关联字段 → 时间字段\n"
        )
    elif file_type == 'views':
        content = (
            f"# -*- coding: utf-8 -*-\n"
            f'"""\n{app_name} 模块视图/视图集\n"""\n'
            f"from rest_framework import viewsets\n"
            f"from rest_framework.response import Response\n\n"
            f"# 遵循规范：类名使用帕斯卡命名法，如 OrderViewSet\n"
            f"class {app_name.capitalize()}ViewSet(viewsets.ViewSet):\n"
            f"    def list(self, request):\n"
            f"        # 视图中只处理请求接收/参数验证/响应返回，业务逻辑在 services.py\n"
            f"        return Response({{'{app_name}': 'List endpoint, call service layer for logic'}})\n"
        )
    elif file_type == 'admin':
        content = (
            f"# -*- coding: utf-8 -*-\n"
            f'"""\n{app_name} 模块 Admin 后台配置\n"""\n'
            f"from django.contrib import admin\n"
            f"# from .models import {app_name.capitalize()}Model\n\n"
            f"# admin.site.register({app_name.capitalize()}Model)\n"
        )
    elif file_type == 'urls':
        content = (
            f"# -*- coding: utf-8 -*-\n"
            f'"""\n{app_name} 模块路由配置\n"""\n'
            f"from django.urls import path, include\n"
            f"from rest_framework.routers import DefaultRouter\n"
            f"from .views import {app_name.capitalize()}ViewSet \n\n"
            f"router = DefaultRouter()\n"
            f"router.register(r'', {app_name.capitalize()}ViewSet, basename='{app_name}')\n\n"
            f"urlpatterns = [\n"
            f"    # 将 ViewSet 注册到根路径，如 /api/{app_name}/ \n"
            f"    path('', include(router.urls))\n"
            f"]\n"
        )
    elif file_type == 'serializers':
        content = (
            f"# -*- coding: utf-8 -*-\n"
            f'"""\n{app_name} 模块序列化器\n"""\n'
            f"from rest_framework import serializers\n"
            f"# from .models import {app_name.capitalize()}Model\n\n"
            f"class {app_name.capitalize()}Serializer(serializers.ModelSerializer):\n"
            f"    # 遵循规范：只负责数据验证和格式转换，禁止写业务逻辑\n"
            f"    class Meta:\n"
            f"        # model = {app_name.capitalize()}Model\n"
            f"        fields = '__all__'\n"
        )
    elif file_type == 'services':
        content = (
            f"# -*- coding: utf-8 -*-\n"
            f'"""\n{app_name} 模块业务逻辑服务层 (Services)\n"""\n\n'
            f"class {app_name.capitalize()}Service:\n"
            f"    @staticmethod\n"
            f"    def create_{app_name}(data):\n"
            f'        """处理创建 {app_name} 的业务逻辑"""\n'
            f"        # 遵循规范：服务层专注于业务逻辑，禁止操作请求/响应对象\n"
            f"        # 遵循规范：函数注释使用 Google 风格\n"
            f"        # Args:\n"
            f"        #    data (dict): 创建 {app_name} 所需的数据\n"
            f"        # Returns:\n"
            f"        #    dict: 处理结果\n"
            f"        \n"
            f"        return {{'status': 'success', 'message': f'{app_name} created successfully'}}\n"
        )
    elif file_type == 'utils':
        content = (
            f"# -*- coding: utf-8 -*-\n"
            f'"""\n{app_name} 模块内部工具函数\n"""\n\n'
            f"def {app_name}_format_data(data):\n"
            f'    """格式化 {app_name} 相关数据"""\n'
            f"    # 遵循规范：函数/变量使用小写蛇形命名法\n"
            f"    return data\n"
        )
    elif file_type == 'tests_init':
        content = "# -*- coding: utf-8 -*-"
    elif file_type == 'init':
        content = ""
    else:
        content = f"# -*- coding: utf-8 -*-\n"

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
        print(f"   [成功] 创建文件: {file_path.name}")
    except Exception as e:
        print(f"   [失败] 写入文件 {file_path.name} 错误: {e}")


def create_django_app(app_name: str):
    """
    通过直接操作文件系统来创建符合规范的 Django 应用。
    """
    target_dir = Path('apps') / app_name
    
    if target_dir.exists():
        print(f"❌ 错误：应用目录 '{target_dir}' 已经存在。请检查应用名是否重复。")
        sys.exit(1)
        
    print(f"--- 步骤 1: 创建应用目录结构到 {target_dir} ---")
    
    # 强制创建应用目录
    target_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n--- 步骤 2: 创建 Django 基础文件和您的规范文件 ---")
    
    # 定义需要创建的文件及其类型（严格按照规范目录结构）
    files_to_create = [
        # 应用根目录文件
        ('init', target_dir / '__init__.py'), # 根目录 __init__.py
        ('apps_config', target_dir / 'apps.py'),
        ('admin', target_dir / 'admin.py'),
        ('models', target_dir / 'models.py'),
        ('views', target_dir / 'views.py'),
        ('urls', target_dir / 'urls.py'),
        
        # 规范要求文件
        ('serializers', target_dir / 'serializers.py'),
        ('services', target_dir / 'services.py'),
        ('utils', target_dir / 'utils.py'),
        
        # 必需子目录文件
        ('init', target_dir / 'migrations' / '__init__.py'), 
    ]
    
    for file_type, file_path in files_to_create:
        create_file_with_content(file_path, app_name, file_type)
        
    print("\n--- 步骤 3: 创建测试目录和文件 ---")

    # 创建 tests 目录及其文件 (符合规范 1.1 的测试目录结构)
    test_dir = target_dir / 'tests'
    test_dir.mkdir(exist_ok=True)
    create_file_with_content(test_dir / '__init__.py', app_name, 'tests_init')
    (test_dir / 'test_models.py').touch()
    (test_dir / 'test_views.py').touch()
    print(f"   [成功] 创建测试目录: {test_dir}/")
    print("   [成功] 创建测试文件骨架 (test_models.py, test_views.py)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python create_app.py <应用名称>")
        sys.exit(1)

    app_name = sys.argv[1].lower()
    
    create_django_app(app_name)
    
    project_config_name = 'yilinbei' 
    
    print("\n\n🎉 应用创建成功！请完成最后配置：")
    print("----------------------------------------------------------------")
    print("⚠️ 注意：这次应用已创建成功，但请手动检查 apps/order 目录，确认文件结构与规范一致。")
    print(f"1. 注册应用：请手动将 '{app_name}.apps.{app_name.capitalize()}Config' 添加到 {project_config_name}/settings/base.py 中的 INSTALLED_APPS 列表。")
    print(f"2. 路由配置：请手动在 {project_config_name}/urls.py 中添加 `path('api/{app_name}/', include('{app_name}.urls'))`。")
    print("----------------------------------------------------------------")