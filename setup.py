#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
初始化脚本 - 用于设置虚拟环境和安装依赖

使用方法:
    python setup.py
"""

import os
import sys
import subprocess
import platform


def run_command(command, cwd=None):
    """运行命令并打印输出"""
    # 增加对命令中路径的引号处理，以防路径中含有空格 (虽然这里用不到，但这是一个好的习惯)
    command_str = ' '.join(f'"{c}"' if ' ' in c else c for c in command)
    print(f"执行: {command_str}")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误: {e.stderr}")
        return False


def main():
    """主函数"""
    print("=== Django项目初始化脚本 ===")
    
    # 检查Python版本
    py_version = platform.python_version()
    print(f"Python版本: {py_version}")
    
    # 创建虚拟环境
    print("\n创建虚拟环境...")
    if not run_command([sys.executable, "-m", "venv", "venv"]):
        print("✗ 虚拟环境创建失败")
        print("提示: 请确保已安装Python虚拟环境模块")
        return
    
    # 确定激活脚本路径和 venv 内部的 python/pip 路径
    venv_path = "venv"
    if platform.system() == "Windows":
        activate_script = os.path.join(venv_path, "Scripts", "activate")
        venv_python_path = os.path.join(venv_path, "Scripts", "python.exe")
        pip_path = os.path.join(venv_path, "Scripts", "pip.exe") # 用于依赖安装
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")
        venv_python_path = os.path.join(venv_path, "bin", "python")
        pip_path = os.path.join(venv_path, "bin", "pip") # 用于依赖安装
    
    print(f"✓ 虚拟环境创建成功")
    print(f"  激活脚本: {activate_script}")
    
    # 升级pip (修改后的逻辑：使用虚拟环境内的 python 解释器来升级 pip 模块)
    print("\n升级pip...")
    # 升级命令：<venv_python_path> -m pip install --upgrade pip
    pip_upgrade_command = [venv_python_path, "-m", "pip", "install", "--upgrade", "pip"]
    
    if not run_command(pip_upgrade_command):
        print("✗ pip升级失败")
        print("⚠️ 注意: 升级失败可能由安全软件或权限锁定引起，后续依赖安装可能失败。")
        # 这里不再直接返回，而是让它尝试安装依赖，因为有时即使升级失败，基础的 pip 仍可用。
    else:
        print("✓ pip升级成功")
    
    # 安装依赖
    print("\n安装项目依赖...")
    # 仍使用 venv\Scripts\pip.exe 来执行安装
    if not run_command([pip_path, "install", "-r", "requirements.txt"]):
        print("✗ 依赖安装失败")
        print("提示: 依赖安装失败可能是因为上一步的 pip 升级错误导致 'pip' 模块损坏。")
    else:
        print("✓ 依赖安装成功")
    
    print("\n=== 设置完成！ ===")
    print("使用说明:")
    if platform.system() == "Windows":
        print(f"  1. 激活虚拟环境: venv\\Scripts\\activate")
    else:
        print(f"  1. 激活虚拟环境: source {venv_path}/bin/activate")
    print("  2. 开始Django项目: django-admin startproject myproject")
    print("  3. 运行开发服务器: python manage.py runserver")


if __name__ == "__main__":
    # 再次提醒用户在运行前清理 venv
    if os.path.exists("venv"):
        print("---")
        print("⚠️ 警告: 检测到 'venv' 文件夹已存在。请先手动删除或确保其未被占用。")
        print("---")
        
    main()