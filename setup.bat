@echo off
REM Windows 一键初始化脚本（PowerShell 建议改用 .ps1）
REM 1) 创建虚拟环境
python -m venv venv

REM 2) 激活虚拟环境（在 PowerShell 中执行： .\venv\Scripts\Activate.ps1）
call .\venv\Scripts\activate.bat

REM 3) 安装开发依赖
pip install -r requirements\dev.txt

REM 4) 代码格式化与导入排序
black .
isort .

REM 5) 代码检查
flake8

echo 初始化完成。请执行：django-admin startproject <项目名> .
echo 然后运行：python create_project.py <项目名>