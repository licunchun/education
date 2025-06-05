# 初始化Flask应用
from flask import Flask
import os
import pymysql
from flask_sqlalchemy import SQLAlchemy

# 配置MySQL数据库连接
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 设置密钥，用于会话

# MySQL数据库配置
# 从环境变量获取数据库连接信息，如果没有则使用默认值
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '3306')
DB_NAME = os.environ.get('DB_NAME', 'education_system')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '87893986lcc')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'connect_args': {'charset': 'utf8mb4'}
}

# 初始化SQLAlchemy
db = SQLAlchemy(app)

# 保持兼容性的数据库连接函数（用于旧的路由代码）
def get_db():
    """
    为了兼容现有代码，提供类似SQLite的接口
    返回一个具有execute方法的包装类
    """
    class DatabaseWrapper:
        def __init__(self):
            from sqlalchemy import create_engine, text
            self.engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
            self.connection = None
            self.text = text
        
        def execute(self, query, params=None):
            if self.connection is None:
                self.connection = self.engine.connect()
            
            # 如果查询已经是text类型，直接使用
            if hasattr(query, 'text'):
                if params:
                    return self.connection.execute(query, params)
                else:
                    return self.connection.execute(query)
            else:
                # 将字符串查询包装为text
                text_query = self.text(query)
                if params:
                    return self.connection.execute(text_query, params)
                else:
                    return self.connection.execute(text_query)
        
        def commit(self):
            if self.connection:
                self.connection.commit()
        
        def rollback(self):
            if self.connection:
                self.connection.rollback()
        
        def close(self):
            if self.connection:
                self.connection.close()
                self.connection = None
    
    return DatabaseWrapper()

# 数据库初始化函数
def init_db():
    """初始化数据库表结构"""
    with app.app_context():
        # 导入所有模型
        from education_system.models.database import (
            Role, User, Major, Class, Student, Teacher, Course, 
            OfferedCourse, CourseSelection, Grade, RegistrationApplication, ApplicationReview
        )
        
        # 创建所有表
        db.create_all()
        print("✅ MySQL数据库表结构创建成功")

# 导入视图模块（放在这里是为了避免循环导入）
from education_system import routes
