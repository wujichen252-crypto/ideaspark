# Django 代码风格与注释规范文档

## 一、代码风格规范

### 1. 文件结构与命名

#### 1.1 项目目录结构

保持与 Django 默认结构一致，按 “功能模块” 拆分应用（App），禁止在单个应用中堆砌所有功能。

**标准结构示例**：

```
project_name/                  # 项目根目录
├── project_name/              # 项目配置目录（与项目同名）
│   ├── __init__.py
│   ├── settings/              # 拆分配置文件（推荐）
│   │   ├── __init__.py
│   │   ├── base.py            # 基础配置
│   │   ├── dev.py             # 开发环境
│   │   └── prod.py            # 生产环境
│   ├── urls.py                # 主路由
│   ├── asgi.py
│   └── wsgi.py
├── apps/                      # 所有应用放在apps目录（可选，便于管理）
│   ├── user/                  # 用户模块应用
│   │   ├── __init__.py
│   │   ├── models.py          # 数据模型
│   │   ├── serializers.py     # DRF序列化器
│   │   ├── views.py           # 视图/视图集
│   │   ├── services.py        # 业务逻辑层
│   │   ├── urls.py            # 应用路由
│   │   ├── tests/             # 测试目录（拆分测试文件）
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   └── test_views.py
│   │   └── utils.py           # 模块内工具函数
│   └── order/                 # 订单模块应用（同上结构）
├── core/                      # 核心公共模块（跨应用复用代码）
│   ├── __init__.py
│   ├── exceptions.py          # 全局异常处理
│   ├── pagination.py          # 分页配置
│   └── utils.py               # 全局工具函数
├── manage.py
└── requirements/              # 拆分依赖文件（推荐）
    ├── base.txt               # 基础依赖
    ├── dev.txt                # 开发依赖（如pytest）
    └── prod.txt               # 生产依赖
```

#### 1.2 文件命名规则

- 所有文件名使用**小写蛇形命名法**（snake_case），禁止大写或驼峰式。

✅ 正确：[user_service.py](http://user_service.py)、[test_order_api.py](http://test_order_api.py)

❌ 错误：[UserService.py](http://UserService.py)、[TestOrderAPI.py](http://TestOrderAPI.py)

- 应用（App）目录名使用**小写单数**（如user而非users，符合 Django 惯例）。

### 2. 命名规范

#### 2.1 变量与函数

- 变量、函数、方法名使用**小写蛇形命名法**，必须见名知意，禁止拼音或无意义缩写。

✅ 正确：user_id、get_active_orders()、calculate_total_price()

❌ 错误：uid（除非全项目统一缩写）、get_dd()、jisuan_zongjia()

- 布尔值变量名建议以is_、has_、can_开头：

✅ 正确：is_active、has_permission、can_delete

#### 2.2 类名

- 类名使用**帕斯卡命名法**（PascalCase，首字母大写），禁止下划线。

✅ 正确：UserViewSet、OrderSerializer、PaymentService

❌ 错误：user_view_set、order_serializer

- 模型类名使用**单数形式**（对应数据库表的 “一行记录”）：

✅ 正确：User、Order（表名可通过class Meta: db_table = "users"指定复数）

#### 2.3 常量

- 常量（模块级别的不可变值）使用**全大写蛇形命名法**，定义在文件顶部。

✅ 正确：MAX_RETRY_COUNT = 3、ORDER_STATUS_PAID = "paid"

#### 2.4 特殊命名

- 避免使用 Python 关键字（如class、def、list）作为标识符。

- 私有变量 / 方法以单下划线_开头（仅内部使用，不强制私有），禁止双下划线（避免名称混淆）：

✅ 正确：_format_phone_number()

❌ 错误：__formatPhone()

### 3. 语法与格式规范

#### 3.1 缩进与换行

- 统一使用**4 个空格**缩进（禁止 Tab，IDE 可配置 “Tab 自动转为 4 空格”）。

- 每行代码长度不超过**88 个字符**（Black 格式化工具默认值，长表达式需换行）。

换行规则：

```
# 正确示例
queryset = User.objects.filter(
    is_active=True,
    create_time__gte=timezone.now() - timedelta(days=30)
).select_related('profile')

total = (
    item.price * item.quantity
    + item.shipping_fee
    - item.discount
)
```

- - 在逗号后换行

- - 操作符前换行

- - 缩进增加一级（后续行与括号对齐）

#### 3.2 空行与空格

- 函数 / 类之间空**2 行**，函数内逻辑块之间空**1 行**：

```
class UserService:
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


    def create_user(self, data):
        # 逻辑块1
        username = data.get("username")
        if not username:
            raise ValueError("用户名必填")

        # 空1行分隔逻辑块
        return User.objects.create(**data)
```

- 运算符前后加空格（赋值、比较、算术等）：

✅ 正确：x = 1 + 2、a == b、if x > 0:

❌ 错误：x=1+2、a==b

- 逗号后加空格（参数、列表元素等）：

✅ 正确：def func(a, b, c):、[1, 2, 3] 

❌ 错误：def func(a,b,c):、[1,2,3]

### 4. 导入规范

- 导入顺序：**标准库 → 第三方库 → 本地应用**，每组之间空 1 行，组内按字母排序。

```
# 标准库
import os
from datetime import datetime

# 第三方库
import requests
from rest_framework.viewsets import ModelViewSet

# 本地应用
from apps.user.models import User
from core.utils import format_time
```

- 禁止使用通配符导入（from module import *），避免命名冲突。

- 导入过长时，使用括号换行：

```
from apps.order.services import (
    OrderCreationService,
    OrderPaymentService,
    OrderRefundService
)
```

- 避免循环导入：若 A 导入 B，B 又导入 A，需通过 “延迟导入”（在函数内导入）或重构代码解决。

### 5. 代码组织规范

#### 5.1 模型（Models）

- 模型字段定义顺序：**主键 → 核心字段 → 关联字段 → 时间字段**，字段注释用verbose_name：

```
class Order(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="订单ID")
    order_no = models.CharField(max_length=32, unique=True, verbose_name="订单编号")  # 核心字段
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="关联用户"
    )  # 关联字段
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "orders"  # 表名用复数
        verbose_name = "订单"
        verbose_name_plural = verbose_name  # 复数名与单数一致（中文无需复数）
        indexes = [models.Index(fields=["order_no"])]  # 索引定义

    def __str__(self):
        return f"Order {self.order_no}"  # 便于Admin显示

    # 模型方法：只处理与自身相关的逻辑
    def is_paid(self):
        """判断订单是否已支付"""
        return self.status == "paid"
```

#### 5.2 视图（Views）

- 优先使用 DRF 的ViewSet/ModelViewSet，通过actions添加自定义接口，避免重复代码。

- 视图中只处理 “请求接收、响应返回、参数验证”，复杂业务逻辑移至[services.py](http://services.py)：

```
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        """处理订单支付（视图层只做参数验证和结果返回）"""
        order = self.get_object()
        payment_data = request.data

        # 调用服务层处理业务
        try:
            result = OrderPaymentService.pay(order, payment_data)
            return Response(result, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
```

#### 5.3 服务层（Services）

- 服务类 / 函数专注于业务逻辑，禁止直接操作请求 / 响应对象（与视图解耦）。

- 服务方法应返回 “原始数据”（字典、模型实例），而非 DRF 响应对象：

```
class OrderPaymentService:
    @staticmethod
    def pay(order, payment_data):
        """
        处理订单支付逻辑
        :param order: Order实例
        :param payment_data: 支付参数（字典）
        :return: 支付结果（字典）
        :raises ValidationError: 支付参数错误时
        """
        if order.is_paid():
            raise ValidationError("订单已支付")

        # 调用支付接口、更新订单状态等逻辑
        payment_result = PaymentAPI.call(
            out_trade_no=order.order_no,
            total_amount=order.total_amount,
            **payment_data
        )

        order.status = "paid"
        order.save()
        return {"success": True, "trade_no": payment_result["trade_no"]}
```

#### 5.4 序列化器（Serializers）

- 序列化器只负责 “数据验证” 和 “格式转换”，禁止在validate方法中写业务逻辑（交给服务层）。

- 区分CreateSerializer和UpdateSerializer（复杂场景下拆分，避免冗余）：

```
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[MinLengthValidator(6)])

    class Meta:
        model = User
        fields = ["username", "phone", "password"]

    def validate_phone(self, value):
        """只做数据格式验证，不涉及业务"""
        if not re.match(r"^1[3-9]\d{9}$", value):
            raise serializers.ValidationError("手机号格式错误")
        return value
```

## 二、代码注释规范

### 1. 注释原则

- 注释需 “准确、简洁、必要”，避免冗余（如 “给变量 a 赋值 1” 这类注释无意义）。

- 注释与代码同步更新（代码修改后，必须更新对应注释）。

- 优先通过 “清晰的命名” 减少注释需求（好的命名比注释更重要）。

### 2. 模块注释（文件头部）

每个 Python 文件顶部需添加模块注释，说明文件功能、作者、创建时间（可选）。

```
# -*- coding: utf-8 -*-
"""
订单模块视图层
负责处理订单相关的API请求，包括创建订单、支付、查询等接口
"""
```

### 3. 类注释

- 类定义下方需添加文档字符串（"""包裹），说明类的作用、核心功能。

- 模型类需说明与其他模型的关系；视图集需说明处理的资源和核心接口。

```
class OrderViewSet(ModelViewSet):
    """
    订单API视图集
    提供订单的CRUD操作，额外包含支付、退款接口
    - GET /api/orders/：查询订单列表
    - POST /api/orders/：创建订单
    - POST /api/orders/{id}/pay/：订单支付
    """
    queryset = Order.objects.all()
    ...
```

### 4. 函数 / 方法注释

使用**Google 风格注释**，包含：

- 功能描述（简要说明方法作用）

- 参数（Args）：参数名、类型、说明

- 返回值（Returns）：类型、说明（无返回值可省略）

- 异常（Raises）：可能抛出的异常及原因（可选）

```
def calculate_order_amount(order_items):
    """
    计算订单总金额（商品金额+运费-折扣）
    
    Args:
        order_items (list[OrderItem]): 订单项列表（包含商品、数量、单价）
    
    Returns:
        dict: 金额明细
            - total: 总金额（float）
            - goods_amount: 商品总金额（float）
            - shipping_fee: 运费（float）
            - discount: 折扣金额（float）
    
    Raises:
        ValueError: 订单项为空时抛出
    """
    if not order_items:
        raise ValueError("订单项不能为空")
    ...
```

#### 特殊场景：

- 简单工具函数（逻辑清晰）可简化注释，只保留功能描述：

```
def format_phone(phone):
    """将手机号格式化为xxx xxxx xxxx"""
    return f"{phone[:3]} {phone[3:7]} {phone[7:]}"
```

### 5. 行内注释（Inline）

- 用于解释 “复杂逻辑的原因”（而非 “做了什么”），放在代码行上方或右侧（需空 2 个空格）。

- 禁止每行代码都加行内注释。

```
# 因第三方API限制，最多重试3次（解释原因）
for i in range(3):
    try:
        return api.call()
    except ApiError:
        if i == 2:  # 最后一次失败则抛出异常（解释特殊处理）
            raise
        time.sleep(1)
```

### 6. 特殊注释标记

- TODO：待完成的工作（需注明负责人和截止时间）

```
# TODO: 李三 2025-11-30 补充订单超时自动取消逻辑
```

- FIXME：已知问题（需注明问题描述和修复建议）

```
# FIXME: 此处可能导致并发问题，建议加分布式锁
order.status = "paid"
order.save()
```

- NOTE：重要说明（如性能优化点、兼容性处理）

```
# NOTE: 这里用select_related减少数据库查询（N+1问题优化）
queryset = Order.objects.select_related("user").all()
```

## 三、协作与工具保障

### 1. 代码格式化工具

- 强制使用**Black**（自动格式化代码，无需争论格式细节）：

```
# 安装
pip install black
# 格式化当前目录
black .
```

- 导入排序使用**isort**（与 Black 兼容）：

```
pip install isort
isort .  # 按规范排序导入
```

### 2. 静态检查工具

- 使用**flake8**检查代码风格问题（PEP 8 合规性）：

```
pip install flake8
flake8 apps/  # 检查指定目录
```

- 复杂项目可使用**pylint**进行深度检查（类设计、变量使用等）。

### 3. 版本控制规范

- 提交代码前必须运行black . && isort . && flake8，确保无格式错误。

- 提交信息格式：[模块名] 操作描述（如[order] 修复支付状态更新bug）。

- 功能开发在独立分支（feature/xxx），修复 bug 在fix/xxx分支，避免直接提交main。

