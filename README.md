# 校园二手书交易平台（campus-market）

- 基于 Flask + SQLite 的校园二手书交易网站，支持用户注册登录、商品发布、浏览与搜索。

**在线演示：** [二手书交易](https://shuijiaofirst123.pythonanywhere.com)

## 功能

- 用户注册 / 登录 / 退出（session 保持登录状态）
- 发布商品（标题、价格、描述，自动记录卖家）
- 商品列表与详情页
- 下单购买/我的订单/删除订单

## 技术栈

- 后端：Python + Flask
- 数据库：SQLite（零配置，适合学习与原型）
- 前端：HTML + Jinja2 模板

## 本地运行

- ```bash
- pip install flask
- python app.py

## 后续计划

商品图片上传
分类与筛选
部署到服务器，提供在线访问
页面截图
## 更新学习记录
2026.10.30
1.datetime方法获取时间
2.数据库合并查找方法:
SELECT 1.? 2.? FROM ... JION ... ON 条件
3.完整守卫顺序(以do_del为例):
①登录检查"account" not in session
②SELECT查目标行看是否为None,为None则redirect
③权限检查 do_del必须是本人进行删除所以要有session.get("account")==row["buyer"]