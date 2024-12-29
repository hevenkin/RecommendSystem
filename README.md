# RecommendSystem

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

> [!WARNING]
>
> 本项目仅供学习参考，未经生产环境测试

## 项目简介

本项目为推荐系统与数据仓库课程的结课设计，一个基于 Django 的药物推荐系统，旨在通过现代推荐算法与数据可视化技术，帮助用户快速获得相关药品推荐。它展示了推荐系统的核心功能和实现方法，适合作为学习和研究推荐系统的入门项目。

## 数据集

* 原始数据集来源于[Kaggle](https://www.kaggle.com/)，数据集链接如下：

* [Medicine_Recommendation](https://www.kaggle.com/datasets/saratchendra/medicine-recommendation/data)

* 此数据集遵循 [CC0: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/) 协议。根据该协议，您可以自由使用、修改和分发该数据集，而无需署名。

* 本项目数据集经过数据预处理以及数据清洗，具体修改内容如下：
  * 替换 'Company_Name' 中 Rating 为 ‘Ratings’ 中 Short-form 对应 Rating；
  * 合并 ‘Medicine_description’ 与 ‘Company_Name’ ；
  * 去除无关列 ‘S.No’, ‘NSE_Symbol’, ‘Industry’ ；
  * 填充缺失的 ‘description’ 值为 ‘Unkown’。

## 实现特性

* **用户管理：**
  * **登陆系统：** 基于 Django 的用户认证系统。
  * **权限控制：** 未登录用户无法访问。
* **推荐系统：** 
  * **支持四种推荐算法：**
    * 基于协同过滤的推荐
    * 基于内容的推荐
    * 基于标签的推荐
    * 基于隐语义的推荐
* **数据可视化：**
  * **支持三种数据可视化：**
    * 不同疾病对应药品数量
    * 药品评分分布
    * 药品数量排名前10的公司
* **界面优化：** 
  * **页面美化：** 基于[Bootstrap](https://getbootstrap.com/), [jQuery](https://jquery.com/)对页面进行美化。
  * **异步加载：** AJAX 实现异步加载内容。
  * **速度优化：** JS及CSS文件保存在本地，加快加载速度，避免无网络演示时无法使用。
  * **友好的用户提醒：** 当用户使用系统时，会适时弹出提示/播放动画效果。

## 技术栈

* **后端：** Django
* **数据库：** MySQL
* **前端：** HTML, [Bootstrap](https://getbootstrap.com/), [jQuery](https://jquery.com/)
* **数据处理**：pandas, numpy
* **推荐系统实现**：scikit-learn

## 环境要求

- [Python](https://www.python.org/)
- [MySQL](https://www.mysql.com/)
- 现代浏览器（本人仅测试在Safari和Chrome中未发现明显错误）

## 快速开始

1. 克隆仓库

   ```bash
   git clone https://github.com/hevenkin/RecommendSystem.git
   cd RecommendSystem
   ```

2. 创建数据库

   ```bash
   mysql -u <USER_NAME> -p
   ```

   ```mysql
   CREATE DATABASE <DATABASE_NAME>;
   ```

3. 配置数据库连接

   按下列代码中注释修改 recommendation_project 中的 settings.py 以连接数据库：

   ```python
   DATABASES = {
       "default": {
           #"ENGINE": "django.db.backends.sqlite3",
           #"NAME": BASE_DIR / "db.sqlite3",
           "ENGINE": "django.db.backends.mysql",
           "NAME": "<DATABASE_NAME>", # 在此处输入上一步你创建的数据库名
           "USER": "<USER_NAME>", # 在此处输入你的数据库用户名
           "PASSWORD": "<USER_PASSWORD>", # 在此处输入你的数据库密码 
           "HOST": "<HOST>", # 在此处输入你的数据库地址（一般为localhost）
           "PORT": "<PORT>", # 在此处输入你的数据库端口（一般为3306）
       }
   }
   ```

4. 初始化数据库

   在终端中运行以下命令初始化数据库和数据：

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py import_drugs
   ```

5. 启动服务器：

   ```bash
   python manage.py runserver
   ```

6. 打开浏览器访问http://127.0.0.1:8000

7. You're done! Enjoy!

## 贡献

欢迎任何形式的贡献！请随意提交 Issue 或 Pull Request。

## 许可证

本项目使用 Apache License 2.0 许可证，详情请查看 [LICENSE](LICENSE) 文件。
