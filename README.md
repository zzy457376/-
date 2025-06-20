# 🎬 Movie Industry Database System（电影行业数据库系统）

本项目是一个用于管理电影、演员、导演、公司、类型、角色等信息的电影行业数据库系统，采用 Flask + MySQL 开发，支持信息的增删改查操作，适用于课程设计、数据库教学与实际管理类场景。

---

## 1. 开发环境

| 项目       | 说明                        |
|------------|-----------------------------|
| 操作系统   | Windows 11 / Ubuntu 22.04   |
| 后端语言   | Python 3.13.0               |
| Web 框架   | Flask                       |
| 前端技术   | JavaScript + HTML           |
| 数据库     | MySQL 8.0                   |
| 监听端口   | 3306                        |
| 依赖管理   | `requirements.txt`          |

---

## 2. 数据库初始化流程

### (1) 环境准备

- 确保已安装 MySQL 8.0 并启动；
- 创建数据库用户并赋予权限（如使用 root）；

### (2) 创建数据库实例

```sql
CREATE DATABASE `电影行业数据库` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
后续的 SQL 语句请参考项目根目录下的 SQL 文件（如 init.sql 或 “sql语句” 文件）。

配置示例（config.py）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': '电影行业数据库',
    'port': 3306
}
示例连接函数（routes/db.py）
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='电影行业数据库',
        port=3306
    )

def close_connection(conn):
    if conn.is_connected():
        conn.close()
3. 测试数据导入
先用sql语句.sql建表，再用test_data.sql插入数据

4. 项目运行步骤与使用方法
(1) 安装依赖

pip install -r requirements.txt
(2) 启动后端

python app.py
启动后会显示：

Running on http://127.0.0.1:5000/
(3) 使用说明
在浏览器中访问上述地址；

使用页面上的“添加”、“编辑”、“删除”、“搜索”按钮管理电影及相关信息；

数据实时存入 MySQL 数据库。

5. 项目目录结构
项目根目录：movie-industry-database/

movie-industry-database/

app.py # Flask 主程序

config.py # 数据库配置文件

routes/ # 后端蓝图目录

__init__.py # 路由蓝图初始化文件

movies.py # 电影相关接口

actors.py # 演员相关接口

... # 其他路由模块，如 directors.py 等

db.py # 数据库连接与关闭

templates/ # HTML 页面模板

movies.html

actors.html

... # 其他模板文件

static/ # 静态资源目录

css/

style.css # 样式文件

js/

movies.js

actors.js

... # 其他 JS 文件

requirements.txt # Python 依赖文件

README.md # 项目说明文件（本文件）

6. 小组成员分工说明
姓名	分工内容
郑致远	数据库语句、前后端代码
高少萱	汇报 PPT 设计、项目文档撰写
方潇砚	概念模型设计、项目文档撰写

7.导出测试数据：movie_industry_dump.sql





