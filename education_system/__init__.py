# 初始化Flask应用
from flask import Flask
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 设置密钥，用于会话

# 配置数据库
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['DATABASE'] = os.path.join(basedir, 'education.db')

# 数据库连接函数
def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row  # 这使得可以通过名称访问列
    return conn

# 初始化数据库
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# 导入视图模块（放在这里是为了避免循环导入）
from education_system import routes
