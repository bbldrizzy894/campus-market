# 校园二手书交易平台（campus-market）

基于 Flask + SQLite 的校园二手书交易网站，支持用户注册登录、商品发布、浏览与搜索。

## 功能

在线演示：https://shuijiaofirst123.pythonanywhere.com
用户注册 / 登录 / 退出（session 保持登录状态）
发布商品（标题、价格、描述，自动记录卖家）
商品列表与详情页
按标题关键词搜索商品
未登录用户访问发布页自动跳转登录

## 技术栈

后端：Python + Flask
数据库：SQLite（零配置，适合学习与原型）
前端：HTML + Jinja2 模板

## 本地运行

1. 克隆仓库：git clone https://github.com/bbldrizzy894/campus-market.git
2. 创建虚拟环境并激活：python -m venv venv → venv\Scripts\activate
3. 安装依赖：pip install flask
4. 运行：python app.py
5. 浏览器访问 http://127.0.0.1:5000

## 项目结构
```text
campus-market/
├── app.py
├── .gitignore
└── templates/
    ├── index.html
    ├── login.html
    ├── publish.html
    └── register.html
```

## 后续计划

商品图片上传
分类与筛选
部署到服务器，提供在线访问
页面截图
2026.10.30
1.datetime方法获取时间
2.数据库合并查找方法:
SELECT 1.? 2.? FROM ... JION ... ON 条件
3.完整守卫顺序(以do_del为例):
①登录检查"account" not in session
②SELECT查目标行看是否为None,为None则redirect
③权限检查 do_del必须是本人进行删除所以要有session.get("account")==row["buyer"]