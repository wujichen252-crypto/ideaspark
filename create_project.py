# 详情查看创建项目目录.md
import os
import sys

def create_dirs_and_files(project_name):
    """
    根据规范文档创建项目的基本目录和文件结构。

    Args:
        project_name (str): 项目名，用于创建 `<项目名>/settings` 配置目录。

    Returns:
        None

    Raises:
        None: 函数内部捕获并打印异常，不向外抛出。
    """
    print(f"开始创建项目骨架: {project_name}...")

    # 定义需要创建的目录和文件（以项目根目录为起点）
    structure = {
        f"{project_name}/settings": ["__init__.py", "base.py", "dev.py", "prod.py"],
        "apps/user": ["__init__.py", "models.py", "serializers.py", "views.py", "services.py", "urls.py", "utils.py"],
        "apps/user/tests": ["__init__.py", "test_models.py", "test_views.py"],
        "core": ["__init__.py", "exceptions.py", "pagination.py", "utils.py"],
        "requirements": ["base.txt", "dev.txt", "prod.txt"],
    }

    # 1. 确保顶层目录存在 (project_name, manage.py, etc.)
    # 假设项目已经运行了 `django-admin startproject project_name .`

    # 2. 遍历并创建自定义目录和文件
    for folder, files in structure.items():
        try:
            os.makedirs(folder, exist_ok=True)
            print(f" - 目录创建成功: {folder}/")
            
            for file in files:
                file_path = os.path.join(folder, file)
                if not os.path.exists(file_path):
                    # 始终以 UTF-8 编码写入，避免 Windows 下出现 'charmap' 编码错误
                    with open(file_path, 'w', encoding='utf-8') as f:
                        # 为 Python 文件添加基本内容
                        if file.endswith('.py') and file != '__init__.py':
                            f.write(
                                '# -*- coding: utf-8 -*-\n"""\n'
                                f"{os.path.basename(file)} 文件功能描述\n"""
                            )
                        elif file.endswith('.txt'):
                            f.write('# 依赖文件\n')
                    print(f"   - 文件创建成功: {file_path}")
        except Exception as e:
            print(f"   - 创建失败 {folder}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python create_project.py <项目名称>")
        print("例如: python create_project.py my_awesome_project")
        sys.exit(1)
    
    project_name = sys.argv[1]
    
    # ----------------------------------------------------
    # 确保运行了 django-admin startproject
    # ----------------------------------------------------
    print("--- 步骤 1: 运行 Django 官方命令 ---")
    if not os.path.exists("manage.py"):
        print("请确保已在当前目录运行:")
        print(f"   django-admin startproject {project_name} .")
        print("之后再运行本脚本。")
        sys.exit(1)
    
    # ----------------------------------------------------
    # 创建自定义结构
    # ----------------------------------------------------
    print("\n--- 步骤 2: 创建自定义规范结构 ---")
    create_dirs_and_files(project_name)

    # ----------------------------------------------------
    # 移动 settings 文件
    # ----------------------------------------------------
    print("\n--- 步骤 3: 移动并清理配置文件 ---")
    old_settings = os.path.join(project_name, "settings.py")
    new_base_settings = os.path.join(project_name, "settings", "base.py")
    
    if os.path.exists(old_settings) and os.path.exists(new_base_settings):
        # 将原始 settings.py 的内容复制到 base.py，统一使用 UTF-8 编码
        with open(old_settings, 'r', encoding='utf-8') as old_f, open(new_base_settings, 'w', encoding='utf-8') as new_f:
            new_f.write(old_f.read())
        
        # 删除原始文件
        os.remove(old_settings)
        print(f" - 移动 {project_name}/settings.py 到 {new_base_settings} 成功。")
    
    print("\n✅ 项目骨架创建完成！")
    print("请记得根据规范修改 settings/__init__.py, dev.py, prod.py 文件内容，并运行 `python manage.py startapp order apps/order` 来创建更多应用。")
    print("最后，不要忘记安装 Black, isort 等工具并配置好 IDE。")