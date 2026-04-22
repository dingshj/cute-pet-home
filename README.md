# 可爱宠物管理系统（Cute Pet Home）

一个基于 Flask 的宠物识别与管理系统，支持宠物品种识别、服务预约、领养管理和宠物商店功能。

## 功能特性

- **宠物品种识别**：上传宠物图片，基于 Oxford-IIIT Pet 数据集训练的模型识别品种（支持模拟模式，无需 GPU）
- **宠物管理**：增删改查宠物信息，支持按种类、品种筛选
- **服务预约**：美容、洗澡、疫苗等服务项目的预约与订单管理
- **领养管理**：领养申请提交与审批流程
- **宠物商店**：宠物商品展示、购物车与订单系统

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Flask 3 |
| 数据库 | SQLite + SQLAlchemy |
| 前端 | Jinja2 模板 + 原生 JS |
| 用户认证 | Flask-Login |
| 宠物识别 | PyTorch（可选，支持 CPU） |

## 项目结构

```
pet-recognition-management/
├── app/
│   ├── __init__.py          # 应用工厂
│   ├── models.py            # 数据库模型
│   ├── routes/              # 路由蓝图
│   │   ├── main.py          # 首页 / 控制台
│   │   ├── recognize.py     # 品种识别
│   │   ├── pets.py          # 宠物管理
│   │   ├── services.py      # 服务预约
│   │   ├── adoption.py      # 领养管理
│   │   ├── shop.py          # 宠物商店
│   │   ├── auth.py          # 用户认证
│   │   └── api.py           # REST API
│   └── services/
│       └── breed_classifier.py  # 品种分类服务
├── scripts/
│   ├── seed_demo.py         # 初始化演示数据
│   ├── seed_shop.py         # 初始化商店数据
│   ├── prepare_oxford_pet.py # 下载并预处理 Oxford Pet 数据集
│   └── train_transfer.py    # 训练品种分类模型
├── instance/                # 数据库与模型文件（不上传 Git）
├── config.py                # Flask 配置
└── run.py                   # 启动入口
```

## 快速开始

### 环境要求

- Python 3.10+
- pip

### 安装依赖

```bash
pip install flask flask-sqlalchemy flask-login pillow torch torchvision
```

### 初始化数据库

```bash
# 创建演示用户和示例数据
python -m scripts.seed_demo
```

### 启动服务

```bash
python run.py
```

访问 http://localhost:5000 ，使用以下账号登录：

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |

### 训练品种识别模型（可选）

```bash
# 下载 Oxford-IIIT Pet 数据集
python -m scripts.prepare_oxford_pet

# 训练迁移学习模型
python -m scripts.train_transfer
```

> 默认使用模拟识别模式，无需下载数据集或训练模型即可体验识别功能。生产环境建议训练真实模型以提高准确率。

## 配置说明

通过环境变量覆盖默认配置：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `SECRET_KEY` | `dev-change-in-production` | Flask 密钥，生产环境务必修改 |
| `DATABASE_URL` | SQLite 本地路径 | 数据库连接 |
| `MODEL_PATH` | `instance/breed_classifier.pt` | 品种识别模型路径 |
| `BREEDS_FILE` | `instance/breeds.txt` | 品种名称列表文件 |
| `MOCK_RECOGNITION` | `true` | 是否启用模拟识别模式 |

## 数据库模型

- **User** — 系统用户（管理员 / 员工）
- **Pet** — 宠物档案（含品种识别结果）
- **ServiceOrder** — 服务预约订单
- **AdoptionRequest** — 领养申请
- **Product / ProductCategory** — 商店商品与分类
- **ShopOrder / ShopOrderItem** — 商店订单

## 品种识别说明

系统支持 37 种猫狗品种的识别（Oxford-IIIT Pet 数据集分类）。

识别模式：
- **真实模型**：加载 `breed_classifier.pt` 进行推理，需要 PyTorch 环境
- **模拟模式**：根据图片路径生成稳定的伪概率，用于无 GPU 环境下的演示

## 许可证

MIT
