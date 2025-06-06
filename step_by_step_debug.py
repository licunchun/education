#!/usr/bin/env python3
# 逐步诊断教育系统问题

import sys
import os
import time

print("🔍 开始逐步诊断教育系统...")

# 添加路径
sys.path.insert(0, 'c:/Users/lcc/Desktop/education')

def test_step(step_name, test_func):
    print(f"\n📋 {step_name}...")
    start_time = time.time()
    try:
        result = test_func()
        end_time = time.time()
        print(f"✅ {step_name} 成功 (耗时: {end_time - start_time:.2f}秒)")
        return result
    except Exception as e:
        end_time = time.time()
        print(f"❌ {step_name} 失败 (耗时: {end_time - start_time:.2f}秒)")
        print(f"   错误: {e}")
        import traceback
        print(f"   详细错误: {traceback.format_exc()}")
        return None

# 步骤1: 测试基础导入
def test_basic_imports():
    from flask import Flask
    import pymysql
    return True

# 步骤2: 测试数据库连接
def test_database_connection():
    import pymysql
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='87893986lcc',
        database='education_system',
        charset='utf8mb4'
    )
    connection.close()
    return True

# 步骤3: 测试Flask应用创建（不导入routes）
def test_flask_app_basic():
    from flask import Flask
    app = Flask(__name__)
    app.secret_key = 'test_key'
    
    @app.route('/')
    def hello():
        return "Hello World"
    
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
    return True

# 步骤4: 测试SQLAlchemy基础配置
def test_sqlalchemy_config():
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    import pymysql
    
    pymysql.install_as_MySQLdb()
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:87893986lcc@localhost:3306/education_system?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy(app)
    return True

# 步骤5: 测试教育系统初始化文件
def test_education_system_init():
    from education_system import app, db
    return True

# 步骤6: 测试模型导入
def test_models_import():
    from education_system.models.database import User, Student, Teacher
    return True

# 步骤7: 测试路由导入
def test_routes_import():
    from education_system import routes
    return True

# 步骤8: 测试完整应用
def test_full_app():
    from education_system import app
    with app.test_client() as client:
        response = client.get('/')
        print(f"   首页响应状态: {response.status_code}")
        return response.status_code == 200

# 运行所有测试
steps = [
    ("基础导入测试", test_basic_imports),
    ("数据库连接测试", test_database_connection),
    ("基础Flask应用测试", test_flask_app_basic),
    ("SQLAlchemy配置测试", test_sqlalchemy_config),
    ("教育系统初始化测试", test_education_system_init),
    ("模型导入测试", test_models_import),
    ("路由导入测试", test_routes_import),
    ("完整应用测试", test_full_app)
]

failed_step = None
for step_name, test_func in steps:
    result = test_step(step_name, test_func)
    if result is None:
        failed_step = step_name
        break

if failed_step:
    print(f"\n💥 在 '{failed_step}' 步骤失败，问题定位成功！")
else:
    print(f"\n🎉 所有测试通过，应用应该可以正常运行")

print("\n🔧 建议检查失败步骤的相关代码文件...")
