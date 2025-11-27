# IdeaSpark Django 后端项目

## 项目简介

这是一个基于 Django 3.2.24 和 Django REST Framework 的后端API项目，采用现代化的项目结构和最佳实践开发。

## 项目特色

- ✅ **多环境配置**：支持开发(dev)、生产(prod)环境配置分离
- ✅ **模块化结构**：按功能模块组织代码，易于维护和扩展
- ✅ **RESTful API**：基于 Django REST Framework 构建
- ✅ **代码规范**：遵循 Django 代码风格和注释规范
- ✅ **开发工具**：集成调试工具栏、代码格式化工具等
- ✅ **跨域支持**：配置 CORS 支持前后端分离开发
- ✅ **用户认证**：内置用户管理和 JWT 认证支持

## 项目结构

```
ideaspark/
├── apps/                    # 应用模块目录
│   └── user/               # 用户模块
│       ├── models.py       # 数据模型
│       ├── serializers.py  # 序列化器
│       ├── views.py       # 视图层
│       ├── urls.py        # 路由配置
│       └── services.py    # 业务逻辑层
├── core/                   # 核心公共模块
│   ├── exceptions.py      # 全局异常处理
│   ├── pagination.py      # 分页配置
│   └── utils.py           # 工具函数
├── ideaspark/              # 项目配置目录
│   ├── settings/          # 配置文件
│   │   ├── base.py       # 基础配置
│   │   ├── dev.py        # 开发环境配置
│   │   └── prod.py       # 生产环境配置
│   ├── urls.py           # 主路由配置
│   ├── wsgi.py           # WSGI 配置
│   └── asgi.py           # ASGI 配置
├── requirements/           # 依赖文件
│   ├── base.txt          # 基础依赖
│   ├── dev.txt           # 开发环境依赖
│   └── prod.txt          # 生产环境依赖
└── static/               # 静态文件目录
```

## 快速开始

### 1. 环境要求

- Python 3.8+
- pip 包管理器
- virtualenv（推荐）

### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装开发环境依赖
pip install -r requirements/dev.txt
```

### 3. 数据库配置

```bash
# 运行数据库迁移
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser
```

### 4. 启动开发服务器

```bash
# 启动开发服务器（默认端口8000）
python manage.py runserver

# 或者指定端口
python manage.py runserver 0.0.0.0:8001
```

### 5. 访问项目

- 开发服务器：http://localhost:8001
- Django 管理后台：http://localhost:8001/admin/
- API 接口：http://localhost:8001/api/user/users/

## API 接口

### 用户模块接口

| 接口 | 方法 | 描述 |
|------|------|------|
| /api/user/users/ | GET | 获取用户列表 |
| /api/user/users/ | POST | 创建新用户 |
| /api/user/users/me/ | GET | 获取当前用户信息 |

### 响应格式

所有API响应采用统一的JSON格式：

```json
{
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
}
```

## 开发环境配置

### 开发工具

- **Black**：代码格式化工具
- **isort**：导入排序工具
- **flake8**：代码风格检查
- **debug_toolbar**：Django调试工具栏
- **django_extensions**：Django扩展工具

### 代码质量

```bash
# 格式化代码
black .

# 排序导入
isort .

# 检查代码风格
flake8 apps/ core/
```

## 生产环境部署

### 环境变量配置

生产环境需要配置以下环境变量：

```bash
# Django 配置
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# 数据库配置
DB_NAME=ideaspark
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Redis 缓存
REDIS_URL=redis://127.0.0.1:6379/1

# 邮件配置（可选）
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

### 生产环境依赖

```bash
pip install -r requirements/prod.txt
```

### 静态文件收集

```bash
python manage.py collectstatic --noinput
```

## 环境切换

项目支持通过环境变量切换配置：

```bash
# 开发环境（默认）
python manage.py runserver

# 生产环境
DJANGO_SETTINGS_MODULE=ideaspark.settings.prod python manage.py check
```

## 扩展开发

### 创建新应用

```bash
# 创建新应用
python manage.py startapp app_name apps/app_name

# 在 settings 中添加应用
# 创建相应的 models.py, serializers.py, views.py, urls.py
```

### 添加新API

1. 在对应应用的 `views.py` 中创建视图
2. 在 `serializers.py` 中创建序列化器
3. 在 `urls.py` 中配置路由
4. 在主项目的 `urls.py` 中包含应用路由

## 注意事项

1. **安全性**：生产环境务必设置强密码的 `SECRET_KEY`
2. **数据库**：生产环境推荐使用 PostgreSQL
3. **静态文件**：生产环境需要配置静态文件服务
4. **日志**：生产环境配置了详细的日志记录
5. **HTTPS**：建议生产环境使用 HTTPS

## 技术支持

如有问题，请检查：

1. 确保所有依赖已正确安装
2. 数据库迁移已执行
3. 环境变量配置正确
4. 查看日志文件获取详细错误信息

## 许可证

此项目采用 MIT 许可证，详见 LICENSE 文件。